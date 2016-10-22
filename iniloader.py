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

import ast
import bananagui
from gettext import gettext as _
import configparser
import io
import re


class _Loader:

    def __init__(self, *args, **kwargs):
        self.parser = configparser.ConfigParser(*args, **kwargs)
        self._loaded = {}

        # These aren't applied right away to avoid circular references.
        self._properties = {}

    def _parse(self, string):
        match = re.search(r'^bananagui.(.*)$', string)
        if match is not None:
            # It's something from bananagui.
            return getattr(bananagui, match.group(1))

        match = re.search(r'^_\((.*)\)$', string)
        if match is not None:
            # It needs to be translated.
            return _(self._parse(match.group(1)))

        if string in self.parser.sections():
            # It's a loadable object.
            self._load_object(string)
            return self._loaded[string]

        # It's a Python literal, like a string literal or a tuple
        # literal. The ast.literal_eval() function is much safer than
        # built-in eval().
        return ast.literal_eval(string)

    def _load_object(self, name):
        if name in self._loaded:
            # This is being called twice.
            return

        data = dict(self.parser[name])  # This will be popped from.
        kwargs = {kwarg_property: self._parse(data.pop(kwarg_property))
                  for kwarg_property in ('parent',)
                  if kwarg_property in data}

        result = self._parse(data.pop('class'))(**kwargs)
        self._properties[name] = data
        self._loaded[name] = result

    def load(self):
        assert not self._loaded, "cannot load twice"

        # Load the objects.
        for sectionname in self.parser.sections():
            self._load_object(sectionname)

        # Apply properties.
        for sectionname, properties in self._properties.items():
            for name, value in properties.items():
                self.loaded[sectionname][name] = self._parse(value)
        return self._loaded


class _NonClosingTextIOWrapper(io.TextIOWrapper):
    """Like io.TextIOWrapper, but without __del__ magic.

    The problem with io.TextIOWrapper is that when its instances are
    destroyed it automatically closes the stream it's wrapping. This
    class doesn't do that.
    """

    # This can't be written as __del__ = object.__del__ because there is
    # no object.__del__.
    def __del__(self):
        pass


def load_ini(source):
    """Load a GUI from source.

    The source can be a string, a dictionary or a file-like object. It
    will be parsed with a configparser.ConfigParser and no
    interpolation.
    """
    loader = _Loader(interpolation=None)
    if isinstance(source, str):
        # It's a string.
        loader.parser.read_string(source)
    elif isinstance(source, dict):
        # It's a dictionary.
        loader.parser.read_dict(source)
    elif isinstance(source, io.TextIOBase):
        # It's a file-like object that returns strings when it's read.
        loader.parser.read_file(source)
    elif isinstance(source, io.IOBase):
        # It's a file-like object that returns bytes when it's read.
        # io.TextIOWrapper can't be used as is because the temporary
        # wrapper is garbage collected when we're done using it and
        # we're not supposed to close the source file.
        loader.parser.read_file(_NonClosingTextIOWrapper(source))
    else:
        raise TypeError("cannot read from a source of type %s"
                        % type(source).__name__)
    return loader.load()


if __name__ == '__main__':
    # testing...
    import pprint
    import bananagui
    from bananagui import utils

    bananagui.load('.tkinter')
    with open('hello-world.ini', 'r') as f:
        widgets = load_ini(f)
    pprint.pprint(widgets)
    bananagui.main()
