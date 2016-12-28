# Copyright (c) 2016 Akuli

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

    [label -> window]
    class = widgets.Label
    text = "Hello World!"

You can preview this file without loading it in Python manually:

    $ yourpython -m bananagui.iniloader the-gui-file.ini

See `yourpython -m bananagui.iniloader --help` for more options, like
using something else instead of tkinter.

When this file is loaded, this module performs these steps:
1. A new namespace dictionary is created for the module.
2. The import at the top are executed in this namespace. These imports
   need to be at the top, and everything before the first section must
   be imports. From imports are fully supported.
3. Each section starts with [a header] and ends to the next header or
   end of file, and the content of sections consists of key=value
   pairs. Now it's time to parse the [window] section. It creates a
   variable called window and sets it to the variable. The value of
   class will be used as constructor and other arguments will be given
   to it as keyword arguments.
4. The next section is otherwise similar, but the header has an arrow
   that points to a parent widget. This calls parent.add() or
   parent.append() depending on the type of the parent. In this case,
   the parent is a Window so add() is called.

In other words, the GUI file above does roughly the same thing as this
Python code:

    from bananagui import widgets

    window = widgets.Window(title="Hello")
    label = widgets.Label(text="Hello World!")
    window.add(label)

The Python code is shorter than the GUI file above, so it doesn't
really make sense to use the guiloader for small GUI's like this. It's
more useful for big projects when it makes sense to separate the GUI to
another file, and load it from a Python file like this:

    import bananagui
    from bananagui import iniloader, mainloop

    bananagui.load('your-favorite-toolkit')
    with open('the-gui-file.ini', 'r') as f:
        widgetdict = iniloader.load(f)

    # Now widgetdict is the namespace dictionary.
    with widgetdict['window'] as window:
        window.on_close.append(mainloop.quit)
        mainloop.run()

The values of the sections can be any Python expressions, including
comments, function calls, list comprehensions and so on. Other
statements (like function and class definitions) are not supported
because the GUI files are meant to be a faster way to write GUI's than
writing Python, not a replacement for Python.
"""

import argparse
import ast
import configparser
import io
import keyword
import sys

import bananagui
from bananagui import mainloop, widgets


_NOT_SET = object()


class ParsingError(SyntaxError):
    r"""An error occurred while parsing.

    This exception behaves like SyntaxError.

    >>> raise ParsingError(
    ...     "oh no", ('test.ini', 123, 3, "this is the line\n"))
    Traceback (most recent call last):
      File "<stdin>", line 2, in <module>
      File "test.ini", line 123
        this is the line
          ^
    ParsingError: oh no
    >>>

    Sometimes lineno and offset aren't available, so they will be None.
    """
    # I didn't find any documentation about constructing SyntaxError,
    # but this seems to work. Here's how I found this:
    #
    #   >>> try:
    #   ...     exec('lol lol')
    #   ... except SyntaxError as e:
    #   ...     args = e.args
    #   ...
    #   >>> args
    #   ('invalid syntax', ('<string>', 1, 7, 'lol lol\n'))
    #   >>> SyntaxError(*args).args
    #   ('invalid syntax', ('<string>', 1, 7, 'lol lol\n'))


def _valid_varname(s):
    """Check if a string is a valid variable name."""
    return s.isidentifier() and not keyword.iskeyword(s)


class _Parser:

    def __init__(self, file):
        self._file = file
        self._filename = getattr(file, 'name', '<unknown>')
        self.namespace = {}

    def parse_imports(self):
        """Parse import statements in the beginning of a file-like object.

        The file's current seek position is left at the end of the import
        statements. The imported modules are added to namespace and the
        number of lines read is returned.
        """
        lines = []
        for line in self._file:
            if line.startswith('[') and line.endswith(']\n'):
                # Oops, we went a bit too far. Let's seek back.
                # The problem with seeking text files is that we need
                # the position in bytes, so we need to find out how
                # many bytes the lines we read are in the file's
                # encoding. Relative seeking with a negative value
                # doesn't seem to work for some reason.
                importbytes = ''.join(lines).encode(self._file.encoding)
                self._file.seek(len(importbytes))
                break
            # More imports.
            lines.append(line)

        # Now we can parse the imports with ast.
        try:
            mod = ast.parse(''.join(lines), filename=self._filename)
        except SyntaxError as error:
            args = error.args
            if sys.version[:2] >= (3, 3):
                # Raising from None is new in Python 3.3.
                error = None
            raise ParsingError(*args) from error
        for node in mod.body:
            if not isinstance(node, (ast.Import, ast.ImportFrom)):
                raise ParsingError(
                    "the top of the ini file can only contain imports",
                    (self._filename, node.lineno, node.col_offset,
                     lines[node.lineno-1]))

        # Importing based on ast.parse's return values turned out to be a
        # lot of work to implement, so I'm lazy and I'll use exec() after
        # making sure there are nothing but imports there. The collections
        # module is written by Raymond Hettinger and it uses exec() for
        # creating namedtuple classes, so it can't be too bad.
        #
        # In other words, it's not an awful hack; it's metaprogramming!
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
        try:
            parser.read_file(self._file)
        # configparser.MissingSectionHeaderError will never be raised
        # because _parse_imports() searches for the beginning of the
        # first section.
        except configparser.ParsingError as e:
            lineno, line = e.errors[0]    # First error.
            lineno += linenostart
            raise ParsingError(
                "invalid ini syntax",
                (self._filename, lineno + linenostart, None, line + '\n'))

        # The sections method does not include the default section in
        # its return value.
        for header in parser.sections():
            self._parse_section(header, parser[header])

    def _parse_section(self, header, section):
        if '->' not in header:
            widgetname = header.strip()
            parentname = None
            parent = None
        elif header.count('->') == 1:
            widgetname, parentname = header.split('->', 1)
            widgetname = widgetname.strip()
            parentname = parentname.strip()
            parent = self.namespace.get(parentname, _NOT_SET)
            if parent is _NOT_SET:
                raise ParsingError(
                    "undefined variable: %r" % parentname,
                    (self._filename, None, None, '[%s]\n' % header))
        else:
            raise ParsingError(
                "headers can contain at most one arrow",
                (self._filename, None, None, '[%s]\n' % header))

        problem = None
        if not _valid_varname(widgetname):
            problem = widgetname
        elif parentname is not None and not _valid_varname(parentname):
            problem = parentname
        if problem is not None:
            raise ParsingError(
                "widget names need to be valid Python variable "
                "names, not %r" % problem,
                (self._filename, None, None, "[%s]\n" % header))

        kwargs = {}
        for unstripped_key, valuesource in section.items():
            key = unstripped_key.strip()
            if key == 'class':
                pass
            elif _valid_varname(key):
                kwargs[key] = eval(valuesource.lstrip(), self.namespace)
            else:
                sourceline = valuesource.partition('\n')[0]
                raise ParsingError(
                    "invalid variable name %r" % key,
                    (self._filename, None, len(key) // 2,
                     "%s = %s\n" % (unstripped_key, sourceline)))

        constsrc = section.get('class', None)
        if constsrc is None:
            raise ParsingError(
                "the [%s] section doesn't define a class" % header,
                (self._filename, None, None, None))
        constructor = eval(constsrc.lstrip(), self.namespace)
        widget = constructor(**kwargs)
        if parent is None:
            pass
        elif isinstance(parent, widgets.Bin):
            parent.add(widget)
        elif isinstance(parent, widgets.Box):
            parent.append(widget)
        else:
            raise TypeError("don't know how to add a child to a %r widget"
                            % type(parent).__name__)
        self.namespace[widgetname] = widget


def load(source) -> dict:
    """Load a GUI from a file object or a string.

    This raises a ParsingError if the source has syntax problems, but
    other errors may also be raised if something goes wrong with
    importing, creating the widgets or something else.

    See help('bananagui.iniloader') for information about BananaGUI's
    ini format and an important security notice.
    """
    if isinstance(source, io.TextIOBase):
        # It's already a file object.
        pass
    elif isinstance(source, str):
        # We need a StringIO object with a name attribute.
        source = io.StringIO(source)
        source.name = '<string>'
    else:
        raise TypeError("don't know how to parse a value of type %r"
                        % type(source).__name__)

    parser = _Parser(source)
    lineno = parser.parse_imports()
    # Copy of keys, '__builtins__' is one of these.
    imported_vars = list(parser.namespace)
    parser.parse_widgets(lineno)
    for name in imported_vars:
        if name in parser.namespace:
            del parser.namespace[name]
    return parser.namespace


def _preview():
    """Simple way to preview BananaGUI ini files."""
    # When running with -m, sys.argv[0] is '__main__' and argparse uses
    # it as the default prog. That's obviously not what we want.
    parser = argparse.ArgumentParser(prog='bananagui.iniloader')
    parser.add_argument(
        'inifile', type=argparse.FileType('r'),
        default=sys.stdin, nargs=argparse.OPTIONAL,
        help="path to the ini file that will be loaded, defaults to stdin")
    parser.add_argument(
        '--load-args', default='.tkinter',
        help="comma-separated list of arguments for bananagui.load()")
    args = parser.parse_args()

    load_args = map(str.strip, args.load_args.split(','))
    bananagui.load(*load_args)

    print("Previewing", args.inifile.name, "...")
    with args.inifile as f:
        widgetdict = load(f)

    windows = {widget for widget in widgetdict.values()
               if isinstance(widget, widgets.Window)}
    if not windows:
        # We can be sure that args.inifile has a name attribute because
        # it's always either sys.stdin or an io.TextIOWrapper returned
        # by argparse.FileType. It's also important not to say "windows
        # is required" to avoid confusion with Windows the operating
        # system.
        print("bananagui.iniloader: no Window objects were found in %s"
              % args.inifile.name, file=sys.stderr)
        sys.exit(1)

    def do_close(window):
        windows.remove(window)
        if not windows:
            mainloop.quit()

    for window in windows:
        window.on_close.append(do_close)

    try:
        mainloop.run()
    finally:
        for window in windows:
            window.destroy()


if __name__ == '__main__':
    _preview()
