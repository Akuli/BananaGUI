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
import copy


# A constant to allow setting None as the value for properties.
_NOTHING = object()


class Property:
    """A Property.

    The Properties are more like properties in GUI toolkits like PyQt
    and GTK+ than Python properties. Add these to class instances on
    __init__, and document them in the class docstring.

    When the value of the property is changed, everything in the
    callback list will be called with the new value as the only
    argument. Note that setting a value equal to the property's current
    value doesn't trigger this.
    """

    # The properties are called explicitly instead of using __set__ and
    # __get__ to avoid interference with other attributes in subclasses,
    # e.g. `label.text = 'hello'` overwrites the property instead of
    # changing its value with descriptor magic. `label.text('hello')`
    # would change the value.

    def __init__(self, default_value):
        """Initialize the Property."""
        self._setter = None
        self._getter = None
        self._value = default_value
        self.callbacks = []

    def set(self, value):
        """Set the Property's value and run the callback functions."""
        if self._setter is None:
            raise ValueError("cannot set the value")
        with self._run_callbacks():
            self._setter(value)
            self._value = value

    def get(self):
        """Return the current value."""
        if self._getter is None:
            return self._value
        return self._getter()

    @contextlib.contextmanager
    def _run_callbacks(self):
        """Run the callbacks if the value changes.

        Get the value in the beginning, yield and get the value at the
        end. If the values are not equal, call the callbacks with the
        new value as the only argument.
        """
        old_value = self.get()
        yield
        new_value = self.get()
        if old_value != new_value:
            for callback in self.callbacks:
                callback(new_value)
