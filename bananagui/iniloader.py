# Copyright (c) 2016-2017 Akuli

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""A way to write GUI's using a simple, ini-like syntax.

This is nice compared to writing the GUI in plain Python when writing
it in Python would be repetitive.

SECURITY NOTE: Don't use this module with untrusted input! The imports
and expressions are evaluated like any other Python code, so it's
possible to do basically anything in them. This module is meant to be
used when writing the GUI in plain Python would be tedious, NOT for
running GUI files that come from random places.

With that out of the way, let's have a look at how this module is
useful using this example GUI file:

    # Hello World GUI for bananagui.iniloader.
    from bananagui import widgets

    [window]
    class = widgets.Window
    title = "Hello"

    [label in window]
    class = widgets.Label
    text = "Hello World!"

You can preview this file without loading it in Python manually:

    $ iniloader preview the-gui-file.ini

Or you can print a tree of the widgets you just created:

    $ iniloader tree the-gui-file.ini

See 'iniloader --help' for more info. You can also use
'yourpython -m bananagui.iniloader' if the iniloader command doesn't
work for some reason.

The file is loaded like this:
1. A new namespace dictionary is created for the module.
2. The imports at the top are executed in this namespace. They need to
   be at the top, and everything before the first section must be
   imports. All import statements are fully supported, and the import
   section ends to the first line starting with '['.
3. Each section starts with [a header] and ends to the next header or
   end of file, and the content of sections consists of key=value pairs.
   Next the window section is parsed. It creates a widgets.Window object
   and sets it to a variable called window. The value of class will be
   used as constructor and other arguments will be given to it as
   keyword arguments.
4. The next section is otherwise similar, but the header is like
   "child in parent". When the child widget has been created,
   parent.add(child) or parent.append(child) will be called depending on
   the type of the parent. In this case, the parent is a Window so
   window.add(label) is called.
5. Imported modules are deleted from the namespace.

In other words, the GUI file above does roughly the same thing as this
Python code:

    from bananagui import widgets

    namespace = {}
    namespace['window'] = widgets.Window(title="Hello")
    namespace['label'] = widgets.Label(text="Hello World!")
    namespace['window'].add(namespace['label'])

The Python code is shorter than the GUI file above, so it doesn't really
make sense to use the iniloader for small GUI's like this. It's more
useful for big projects, because then the GUI can be in a separate file
that is loaded from Python like this:

    from bananagui import iniloader, load_wrapper, mainloop

    load_wrapper('whatever you want')
    with open('the-gui-file.ini', 'r') as f:
        widgetdict = iniloader.load(f)

    # Now widgetdict is the namespace dictionary.
    widgetdict['window'].on_close.connect(mainloop.quit)
    mainloop.run()

Section names and the keys in the sections must be valid variable
names, except the class key that specifies the constructor.

The values of the sections can be any Python expressions, including
comments, function calls, list comprehensions and so on. Other
statements like function and class definitions are not supported because
the GUI files are meant to be a faster way to write GUI's than writing
Python, not a replacement for Python.

It's also possible to use multiline values by indenting everything
except the first line:

    [multiline_label]
    class = widgets.Label
    text = (
      "Hello "
      "multiline "
      "world!")
"""

import argparse
import ast
import configparser
import io
import keyword
import re
import shutil
import sys

from bananagui import load_wrapper, mainloop, widgets

__all__ = ['ParsingError', 'load', 'loads', 'main']


class ParsingError(Exception):
    """An error occurred while parsing.

    This is not the only error that can be raised while parsing. This
    error is typically raised if the non-Python syntax of the file is
    invalid.
    """

    def __init__(self, message, filename=None, lineno=None,
                 line=None, *, add_repr=True):
        # Calling super().__init__() creates an args attribute that we
        # don't need, so we don't call that. This is documented
        # behavior, not a random implementation detail.
        self.message = message
        self.filename = filename
        self.lineno =  lineno
        if line is not None and add_repr:
            line = repr(line.strip())
        self.line = line

    def __str__(self):
        result = self.message
        if self.filename is not None:
            result += "\nfile %r" % self.filename
            if self.lineno is not None:
                result += ", line %d" % self.lineno
        if self.line is not None:
            result += "\n  %s" % self.line
        return result


class _IniParser:

    def __init__(self, file):
        self._file = file
        self._filename = getattr(file, 'name', '<unknown>')
        self.namespace = {}

    def parse_imports(self):
        """Parse import statements in the beginning of a file-like object.

        The file's current seek position is left at the end of the
        import statements. The imported modules are added to namespace
        and the number of lines read is returned.
        """
        lines = []
        for line in self._file:
            if line.startswith('['):
                # Oops, we went a bit too far. Let's seek back.
                # The problem with seeking text files is that we need
                # the position in bytes, so we need to find out how many
                # bytes the lines we read are in the file's encoding.
                # Relative seeking with a negative value doesn't seem to
                # work for some reason.
                if self._file.encoding is None:
                    # e.g. StringIO
                    seekcount = len(''.join(lines))
                else:
                    seekcount = len(''.join(lines).encode(self._file.encoding))
                try:
                    self._file.seek(seekcount)
                except io.UnsupportedOperation:
                    # We can't seek the file, it's probably sys.stdin.
                    # We need to turn the whole thing into a StringIO.
                    fakefile = io.StringIO()
                    fakefile.write(line)
                    shutil.copyfileobj(self._file, fakefile)
                    fakefile.seek(0)
                    self._file = fakefile
                break
            lines.append(line)

        # Now we can parse the imports with ast.
        mod = ast.parse(''.join(lines), filename=self._filename)
        for node in mod.body:
            if not isinstance(node, (ast.Import, ast.ImportFrom)):
                raise ParsingError(
                    "the top of the ini file can only contain imports",
                    self._filename, node.lineno, lines[node.lineno-1])

        # Importing based on ast.parse's return values turned out to be a
        # lot of work to implement, so I'm lazy and I'll use exec() after
        # making sure there are nothing but imports there. The collections
        # module is written by Raymond Hettinger and it uses exec() for
        # creating namedtuple classes, so David Beazley thought that it
        # can't be too bad and used exec().
        #
        # In other words, it's not an awful hack. It's metaprogramming!
        exec(''.join(lines), self.namespace)
        return len(lines)

    def parse_widgets(self, linenostart):
        """Parse the rest of the file after running parse_imports().

        linenostart should be the return value from parse_imports().
        """
        # We can't use inline_comment_prefixes or interpolation because
        # they would collide with the values because they are Python
        # expressions. We also need a default section name that can't
        # collide with other section names, and a section name with a
        # space does this well because section names need to be valid
        # Python identifiers.
        parser = configparser.ConfigParser(
            default_section='the default', interpolation=None,
            delimiters=['='], comment_prefixes=['#'])

        # configparser.MissingSectionHeaderError will never be raised
        # because _parse_imports() searches for the beginning of the
        # first section, so we don't need to handle that.
        try:
            parser.read_file(self._file)
        except configparser.ParsingError as e:
            # We could edit the exception to correct its line numbers,
            # but it's easier to just raise our own ParsingError.
            lineno, line = e.errors[0]    # First error.
            lineno += linenostart
            if sys.version_info[:2] >= (3, 3):
                # Raising from None is new in Python 3.3.
                e = None
            raise ParsingError("invalid ini syntax", self._filename,
                               lineno, line, add_repr=False) from e

        # The sections method does not include the default section in
        # its return value.
        for header in parser.sections():
            self._parse_section(header, parser[header])

    def _check_varname(self, name, *args, must_exist=True, **kwargs):
        """Check if a variable name is valid.

        Raise ParsingError if the name is not valid. If must_exist is
        True, also make sure the name is in the namespace. Other
        arguments are passed to ParsingError.
        """
        if keyword.iskeyword(name) or not name.isidentifier():
            raise ParsingError("invalid variable name %r" % name,
                               self._filename, *args, **kwargs)
        if must_exist and name not in self.namespace:
            raise ParsingError("undefined variable %r" % name,
                               self._filename, *args, **kwargs)

    def _parse_section(self, header, section):
        real_header = '[%s]' % header
        parts = header.split()
        if len(parts) == 1:
            widgetname = header.strip()
            self._check_varname(widgetname, line=real_header,
                                must_exist=False)
            parentname = None
            parent = None
        elif len(parts) == 3:
            widgetname, in_, parentname = parts
            if in_ != 'in':
                raise ParsingError(
                    "the second word of 3-word headers must be 'in'",
                    self._filename, line=real_header)
            self._check_varname(widgetname, line=real_header,
                                must_exist=False)
            self._check_varname(parentname, line=real_header)
            parent = self.namespace[parentname]
        else:
            raise ParsingError(
                "headers can contain one or three words, not %d" % len(parts),
                self._filename, line=real_header)

        kwargs = {}
        for key, valuesource in section.items():
            if key.strip() == 'class':
                continue
            sourceline = valuesource.split('\n')[0]
            self._check_varname(key.strip(), line=key + " = " + sourceline,
                                must_exist=False)
            kwargs[key.strip()] = eval(valuesource.lstrip(), self.namespace)

        class_source = section.get('class', None)
        if class_source is None:
            raise ParsingError(
                "the %s section doesn't define a class" % real_header,
                self._filename)
        constructor = eval(class_source.lstrip(), self.namespace)
        widget = constructor(**kwargs)
        if parent is None:
            pass
        elif isinstance(parent, widgets.Bin):
            parent.add(widget)
        elif isinstance(parent, widgets.Box):
            parent.append(widget)
        else:
            cls = type(parent)
            raise TypeError("don't know how to add a child to a %s.%s widget"
                            % (cls.__module__, cls.__name__))
        self.namespace[widgetname] = widget


def load(file) -> dict:
    """Load a GUI from a file object.

    See help('bananagui.iniloader') for information about BananaGUI's
    ini format and an important security notice.

    This raises a ParsingError if the file has syntax problems, but
    other errors may also be raised if something goes wrong with
    importing, creating the widgets or something else.
    """
    parser = _IniParser(file)
    lineno = parser.parse_imports()
    # Copy of keys, '__builtins__' is one of these.
    imported_vars = list(parser.namespace)
    parser.parse_widgets(lineno)
    for name in imported_vars:
        if name in parser.namespace:
            del parser.namespace[name]
    return parser.namespace


def loads(string) -> dict:
    """Like load(), but for strings."""
    fakefile = io.StringIO(string)
    fakefile.name = '<string>'  # for error messages
    return load(fakefile)


# Simple command-line interface.

def main():     # pragma: no cover
    """Run the command-line interface.

    This uses sys.argv and may use sys.exit().
    """
    parser = argparse.ArgumentParser(add_help=False)

    generalgroup = parser.add_argument_group("General options")
    generalgroup.add_argument(
        '-h', '--help', action='help',
        help="Display this help message and exit.")
    generalgroup.add_argument(
        'action', choices=['tree', 'preview'],
        help=("Choose what to do. 'tree' dumps a tree of widgets in "
              "INIFILE using bananagui.widgettree, and 'preview' loads "
              "and runs INIFILE."))
    generalgroup.add_argument(
        'inifile', metavar='INIFILE', type=argparse.FileType('r'),
        help="Path to the BananaGUI ini file or - for stdin.")

    treegroup = parser.add_argument_group("Tree options")
    treegroup.add_argument(
        '-a', '--ascii-only', action='store_true',
        help="Use ASCII characters only.")
    treegroup.add_argument(
        '-o', '--outfile', type=argparse.FileType('w'), default=sys.stdout,
        help="Dump to this file instead of stdout.")

    previewgroup = parser.add_argument_group("Preview options")
    previewgroup.add_argument(
        '-w', '--wrapper', default='tkinter',
        help=("The argument for bananagui.load_wrapper(). "
              "Defaults to %(default)r."))

    # This isn't using subparsers because I want to display general options,
    # tree options and preview options all in the same --help.
    args = parser.parse_args()
    if args.action == 'tree':
        if args.wrapper != 'tkinter':
            parser.error("cannot use -w/--wrapper with tree")

        # I think a local import makes sense here because this way the
        # iniloader can be used even if widgettree doesn't work for some
        # reason.
        from bananagui import widgettree
        load_wrapper('dummy')
        with args.inifile as f:
            windows = {widget for widget in load(f).values()
                       if isinstance(widget, widgets.Window)}
        with args.outfile as f:
            for window in windows:
                widgettree.dump(window, file=f, ascii_only=args.ascii_only)

    if args.action == 'preview':
        if args.ascii_only:
            parser.error("cannot use -a/--ascii-only with preview")
        if args.outfile is not sys.stdout:
            parser.error("cannot use -o/--outfile with preview")

        load_wrapper(args.wrapper)
        with args.inifile as f:
            windows = {widget for widget in load(f).values()
                       if isinstance(widget, widgets.Window)}
        if not windows:
            # It's important not to say "this needs windows" to avoid
            # confusion with Windows the operating system.
            print("iniloader: no Window objects were found in %s"
                  % args.inifile.name, file=sys.stderr)
            sys.exit(1)

        def do_close(window):
            windows.remove(window)
            if not windows:
                mainloop.quit()

        for window in windows:
            window.on_close.connect(do_close, window)
        mainloop.run()


if __name__ == '__main__':  # pragma: no cover
    main()
