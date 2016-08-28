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

"""A base object for BananaGUI widgets."""

from bananagui import exceptions
from bananagui.core import properties, signals


class ObjectBase:
    """An object that allows using properties and signals with subscripting."""

    def __prop_or_sig(self, name):
        result = type(self)
        try:
            for attribute in name.split('.'):
                result = getattr(result, attribute)
        except AttributeError as e:
            raise exceptions.NoSuchPropertyOrSignal(name) from e
        if not isinstance(result, (properties.Property, signals.Signal)):
            raise TypeError("expected a BananaGUI property or signal, got %r"
                            % (result,))
        return result

    def __setitem__(self, property_or_signal_name, value):
        """Set the value of a property or a signal's callback list."""
        self.__prop_or_sig(property_or_signal_name).set(self, value)

    def __getitem__(self, property_or_signal_name):
        """Return the value of a property or a signal's callback list."""
        return self.__prop_or_sig(property_or_signal_name).get(self)

    def raw_set(self, propertyname, value):
        """Set a property's value directly to its cache."""
        self.__prop_or_sig(propertyname).raw_set(self, value)

    def raw_get(self, propertyname):
        """Get a property's value directly from its cache."""
        return self.__prop_or_sig(propertyname).raw_get(self)

    def emit(self, signalname):
        """Emit a signal."""
        self.__prop_or_sig(signalname).emit(self)
