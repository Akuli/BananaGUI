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

"""BananaGUI wrapper loader."""

import importlib

import bananagui.base
import bananagui.wrappers  # noqa


class _WrapperLoader:

    def __init__(self):
        """Initialize the loader."""
        self._not_loaded = {}  # {name: (base, wrapper), ...}
        self._loaded = {}      # {name: loaded_class, ...}

    def _load_class(self, name):
        if name in self._loaded:
            return

        baseclass, wrapperclass = self._not_loaded[name]
        bases = [baseclass]
        if wrapperclass is not None:
            # The wrapper comes after the base, so the base can call it
            # with super().
            bases.append(wrapperclass)

        for base in getattr(baseclass, '_bananagui_bases', ()):
            assert isinstance(name, str), \
                "_bananagui_bases should contain strings"
            self._load_class(base)
            bases.append(self._loaded[base])

        self._loaded[name] = type(
            baseclass.__name__,
            tuple(bases),
            {'__doc__': baseclass.__doc__, '__module__': 'bananagui'},
        )

    def load(self, wrappermodule):
        """Load the wrapper's classes, functions and other values."""
        for name in dir(bananagui.base):
            if name.startswith('_'):
                # Something non-public.
                continue
            baseclass = getattr(bananagui.base, name)
            if not isinstance(baseclass, type):
                # It's not a class.
                continue
            wrapperclass = getattr(wrappermodule, name, None)
            self._not_loaded[name] = (baseclass, wrapperclass)

        for name in self._objects:
            self._load_class(name)

    def install(self, target):
        """Copy the loaded values to target's attributes."""
        for name, value in self._loaded.items():
            setattr(target, name, value)


_wrapper_loaded = False


def load(*guiwrappers):
    """Load a BananaGUI wrapper module.

    The wrappers should be Python module names. If they are relative,
    they will be treated as relative to bananagui.wrappers. For example,
    '.tkinter' is equivalent to 'bananagui.wrappers.tkinter'.

    If multiple wrappers are given, attempt to load each one until
    loading one of them succeeds.
    """
    if not guiwrappers:
        raise ValueError("specify at least one wrapper")

    if len(guiwrappers) == 1:
        # Load the wrapper.
        global _wrapper_loaded

        if _wrapper_loaded:
            raise RuntimeError("a wrapper cannot be loaded twice")

        # Automatically importing parent modules is new in Python 3.3.
        # This is also why bananagui.wrappers is imported in the
        # beginning of this file.
        wrappermodule = importlib.import_module(
            guiwrappers[0], 'bananagui.wrappers')

        loader = _WrapperLoader()
        loader.load(wrappermodule)
        loader.install(bananagui)
        bananagui.MainLoop.init()
        _wrapper_loaded = True

    else:
        # Attempt to load each wrapper.
        for wrapper in guiwrappers:
            try:
                load(wrapper)
                return
            except ImportError:
                pass
        raise ImportError("cannot load any of the requested GUI wrappers")
