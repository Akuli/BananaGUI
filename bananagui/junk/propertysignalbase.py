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

"""The core of BananaGUI."""

import contextlib

from bananagui import exceptions, properties, signals


class PropertySignalBase:
    """A base class for using BananaGUI properties and signals."""

    def __get(self, name, *types):
        assert types, "specify at least one type"

        result = type(self)
        try:
            for attribute in name.split('.'):
                result = getattr(result, attribute)
        except AttributeError as e:
            raise exceptions.NoSuchPropertyOrSignal(name) from e

        if not isinstance(result, types):
            if len(types) == 1:
                message = "expected type %s, got %r"
            else:
                message = "expected any type from %s; got %r"
            types = ', '.join(t.__name__ for t in types)
            raise TypeError(message % (types, result))

        return result

    def __setitem__(self, name, value):
        """Set the value of a property or a signal's callback list."""
        prop_or_sig = self.__get(name, properties.Property, signals.Signal)
        prop_or_sig.set(self, value)

    def __getitem__(self, name):
        """Return the value of a property or a signal's callback list."""
        prop_or_sig = self.__get(name, properties.Property, signals.Signal)
        return prop_or_sig.get(self)

    def raw_set(self, name, value):
        """Set a property's value directly to its cache."""
        self.__get(name, properties.Property).raw_set(self, value)

    def emit(self, name, **kwargs):
        """Emit a signal."""
        self.__get(name, sig=True).emit(self, **kwargs)

    def blocked(self, name):
        """Block a signal temporarily.

        Use this as a context manager.
        """
        return self.__get(name, sig=True).blocked(self)
