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

"""BananaGUI properties."""

import weakref

from bananagui import exceptions, signals


class Property:
    """A basic property.

    The properties are not like Python properties with descriptor magic.
    They are more like properties in large GUI toolkits like Qt and
    GTK+.
    """

    def __init__(self, name, *, allow_none=False, default=None,
                 getdefault=None, required_type=object, checker=None,
                 add_changed=True):
        """Initialize the property.

        See the set and get docstrings for explanations about the
        arguments.
        """
        if default is not None and getdefault is not None:
            raise ValueError("don't specify both default and getdefault")
        if checker is not None and required_type is not object:
            raise ValueError("don't specify both checker and required_type")

        self._name = name
        self._allow_none = allow_none
        self._default = default
        self._getdefault = getdefault
        self._required_type = required_type
        self._checker = checker

        self._values = weakref.WeakKeyDictionary()
        if add_changed:
            self.changed = signals.Signal(name)

    def raw_set(self, widget, value):
        """Set the value directly to the dictionary of set values.

        This also emits the changed signal.
        """
        old_value = self._values[widget]
        self._values[widget] = value
        if hasattr(self, 'changed'):
            self.changed.emit(widget, old_value=old_value, new_value=value)

    def set(self, widget, value):
        """Set the value and emit the changed signal.

        Setting a property's value works like this:
          - Make sure the widget's type has a setter. The setter is
            TYPE_OF_WIDGET._bananagui_set_NAME.
          - If allow_none is false, make sure the value is not None.
          - If the value is not None, make sure it's an instance of
            required_type and run checker(value). The checker should
            raise an exception if the value is not correct.
          - Call the setter with the widget and the converted value
            as arguments.
          - Call self.raw_set().
        """
        try:
            setter = getattr(type(widget), '_bananagui_set_' + self._name)
        except AttributeError as e:
            raise exceptions.NotSettable(self._name) from e

        if value is None:
            # Bypass the converting, type checking and whitelist
            # checking.
            if not self._allow_none:
                raise ValueError("None is not an allowed value")
        else:
            if not isinstance(value, self._required_type):
                raise TypeError("expected type %s, got %r"
                                % (self._required_type.__name__, value))
            if self._checker is not None:
                self.checker(value)

        setter(widget, value)
        self.raw_set(widget, value)

    def get(self, widget):
        """Get the value.

        Try to get the value from the dictionary of values that are set.
        If it fails, use getdefault or default. getdefault will be
        called without arguments.
        """
        try:
            # Get the value from the dictionary.
            value = self._values[widget]
        except KeyError:
            # Create a new value and set it into the dictionary.
            if self._getdefault is not None:
                value = self._getdefault()
            else:
                value = self._default
            self._values[widget] = value
        return value
