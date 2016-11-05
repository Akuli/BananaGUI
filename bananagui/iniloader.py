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
import collections
import configparser
import gettext
import io

import bananagui


class _Loader:

    def __init__(self):
        self.parser = configparser.ConfigParser(interpolation=None)
        self.loaded = {}

        # These aren't applied right away to avoid circular references.
        self.apply_later = collections.defaultdict(dict)

    def parse_node(self, node):
        if isinstance(node, ast.NameConstant):
            return node.value
        if isinstance(node, ast.Str):
            return node.s
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.List):
            return list(map(self.parse_node, node.elts))
        if isinstance(node, ast.Tuple):
            return tuple(map(self.parse_node, node.elts))
        if isinstance(node, ast.Dict):
            keys = map(self.parse_node, node.keys)
            values = map(self.parse_node, node.values)
            return dict(zip(keys, values))
        if isinstance(node, ast.Attribute):
            return getattr(self.parse_node(node.value), node.attr)
        if isinstance(node, ast.Call):
            function = self.parse_node(node.func)
            args = map(self.parse_node, node.args)
            kwargs = {keyword.arg: self.parse_node(keyword.value)
                      for keyword in node.keywords}
            return function(*args, **kwargs)
        if isinstance(node, ast.Name):
            if node.id == '_':
                # The translating function.
                return gettext.gettext
            if node.id == 'gui':
                return bananagui.gui
            if node.id == 'bananagui':
                return bananagui
            self.load_object(node.id)
            return self.loaded[node.id]
        raise ValueError("unknown value type: %s" % type(node).__name__)

    def parse_source(self, line):
        module = ast.parse(line.strip())
        if len(module.body) != 1:
            raise ValueError("expected one expression, line %r contains "
                             "%d expressions" % (line, len(module.body)))
        return self.parse_node(module.body[0].value)

    def load_object(self, name):
        if name in self.loaded:
            # This is being called twice.
            return

        kwargs = {}
        for propertyname, valuesource in self.parser[name].items():
            if propertyname in {'child', 'children'}:
                # The value can't be set with kwargs because we would
                # end up with circular references.
                self.apply_later[name][propertyname] = valuesource
            elif propertyname not in {'class'}:
                # The name doesn't have a special meaning.
                kwargs[propertyname] = self.parse_source(valuesource)

        constructor = self.parse_source(self.parser[name]['class'])
        self.loaded[name] = constructor(**kwargs)

    def load(self):
        for name in self.parser.sections():
            self.load_object(name)

        # Apply properties.
        for name, properties in self.apply_later.items():
            widget = self.loaded[name]
            for propertyname, source in properties.items():
                widget[propertyname] = self.parse_source(source)


def load_ini(source) -> dict:
    """Load a GUI from source.

    The source can be a string or a file object. It will be parsed with
    configparser.ConfigParser. It may be closed if it's a file object.
    Closing an already closed file does nothing so you can just use a
    with statement normally.
    """
    if not hasattr(bananagui, 'gui'):
        raise RuntimeError("bananagui.load() wasn't called before "
                           "calling bananagui.iniloader.load_ini()")

    loader = _Loader()
    if isinstance(source, str):
        loader.parser.read_string(source)
    elif isinstance(source, io.TextIOBase):
        loader.parser.read_file(source)
    elif isinstance(source, io.IOBase):
        # ConfigParser expects strings, but the file object gives us
        # bytes.
        loader.parser.read_file(io.TextIOWrapper(source))
    else:
        raise TypeError("cannot read from a source of type %s"
                        % type(source).__name__)
    loader.load()
    return loader.loaded
