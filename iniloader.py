import ast
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


def load_ini(source):
    """Load a GUI from source.

    The source can be a string, a dictionary or a file-like object. It
    will be parsed with a configparser.ConfigParser and no
    interpolation.
    """
    loader = _Loader(interpolation=None)
    if isinstance(source, str):
        loader.parser.read_string(source)
    elif isinstance(source, dict):
        loader.parser.read_dict(source)
    elif isinstance(source, io.TextIOBase):
        loader.parser.read_file(source)
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
        widgets = load(f)
    pprint.pprint(widgets)
    widgets['box'].add_start(result['label'], expand=True)
    widgets['box'].add_start(result['button'])
    bananagui.main()
    bananagui.MainLoop.run()
