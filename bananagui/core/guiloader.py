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

"""Loader for GUI toolkit wrappers."""

import functools
import itertools
import types

import bananagui.gui


_ORIGINAL_GUI_DIR = dir(bananagui.gui)


class _Loader:

    def __init__(self, basemodule, wrappermodule):
        """Initialize the loader.

        Call the .load() method to actually load the wrapper.
        """
        self._basemodule = basemodule
        self._wrappermodule = wrappermodule
        self._classes = {}
        self._functions = {}
        self._other_values = {}
        self._loaded = False

    def _load_class(self, classname):
        if classname in self._classes:
            # The same class is loaded twice for some reason.
            return

        baseclass = getattr(self._basemodule, classname)
        wrapperclass = getattr(self._wrappermodule, classname, None)

        # Create a list of the bases.
        bases = [baseclass]
        if wrapperclass is not None:
            bases.insert(0, wrapperclass)
        if hasattr(baseclass, 'BASES'):
            for base in baseclass.BASES:
                if isinstance(base, str):
                    # Use another class loaded by this method.
                    self._load_class(base)
                    base = self._classes[base]
                bases.append(base)
            del baseclass.BASES

        # Create the mixin class.
        self._classes[classname] = type(
            baseclass.__name__,
            tuple(bases),
            {'__doc__': baseclass.__doc__, '__module__': 'bananagui.gui'},
        )

    def _load_function(self, functionname):
        if functionname in self._functions:
            # This is called twice with the same function name.
            return

        basefunction = getattr(self._basemodule, functionname)
        try:
            wrapperfunction = getattr(self._wrappermodule, functionname)
        except AttributeError:
            # The wrapper does not have this function.
            self._functions[functionname] = basefunction
            return

        @functools.wraps(basefunction)
        def result(*args, **kwargs):
            # Call the base and the wrapper.
            basefunction(*args, **kwargs)
            return wrapperfunction(*args, **kwargs)

        self._functions[functionname] = result

    def load(self):
        """Load the wrapper's classes, functions and other values."""
        if self._loaded:
            # This is called twice for some reason.
            return

        for name in dir(self._basemodule):
            if name.startswith('_'):
                # Something non-public.
                continue

            value = getattr(self._basemodule, name)
            if isinstance(value, type):
                # It's a class.
                self._load_class(name)
            elif isinstance(value, types.FunctionType):
                # It's a function.
                self._load_function(name)
            else:
                # It's something else.
                self._other_values[name] = value

        # Maybe the wrapper has something that the base doesn't have?
        base_dir = dir(self._basemodule)
        for name in dir(self._wrappermodule):
            if name not in base_dir:
                if name.startswith('_'):
                    continue
                self._other_values[name] = getattr(self._wrappermodule, name)

        self._loaded = True

    def install(self, target):
        """Copy the loaded values to target's attributes."""
        if not self._loaded:
            raise ValueError("call load() before install()")
        for name, value in itertools.chain(self._classes.items(),
                                           self._functions.items(),
                                           self._other_values.items()):
            setattr(target, name, value)


def load_wrapper(basemodule, wrappermodule):
    """Clear bananagui.gui and load wrappermodule into it."""
    for name in dir(bananagui.gui):
        if name not in _ORIGINAL_GUI_DIR:
            delattr(bananagui.gui, name)

    loader = _Loader(basemodule, wrappermodule)
    loader.load()
    loader.install(bananagui.gui)
