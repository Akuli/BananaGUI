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


class BaseObject:
    """An object that allows using properties and signals with subscripting.

    To access a changed signal of a property, you can subscript with
    'propertyname.changed'.
    """

    @classmethod
    def __prop_or_sig(cls, propertyname_or_signalname):
        """Return a property or a signal."""
        property_or_signal = cls
        for attribute in str(propertyname_or_signalname).split('.'):
            property_or_signal = getattr(property_or_signal, attribute)
        return property_or_signal

    def __setitem__(self, propertyname_or_signalname, value):
        """Set the value of a property or a signal's callback list."""
        self.__prop_or_sig(propertyname_or_signalname).set(self, value)

    def __getitem__(self, propertyname_or_signalname):
        """Return the value of a property or a signal's callback list."""
        return self.__prop_or_sig(propertyname_or_signalname).get(self)

    def emit(self, signalname, *args):
        """Emit a signal with args."""
        self.__prop_or_sig(signalname).emit(*args)
