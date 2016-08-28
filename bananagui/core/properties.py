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

"""A property system for BananaGUI."""

import weakref

from bananagui import exceptions
from bananagui.core import signals


# Allow None as a non-default value.
_NOTHING = object()


class Property:
    """A basic property.

    The properties are not like Python properties with descriptor magic.
    They are more like properties in large GUI toolkits like Qt and
    GTK+.
    """

    def __init__(self, name, *,
                 converter=lambda x: x,
                 allow_none=False,
                 default=_NOTHING,
                 getdefault=None,
                 required_type=object,
                 whitelist=None):
        """Initialize the property.

        See the set and get docstrings for explanations about the
        arguments.
        """
        if default is not _NOTHING and getdefault is not None:
            raise ValueError("specify default or getdefault, not both")

        self._name = name
        self._converter = converter
        self._allow_none = allow_none
        self._default = default
        self._getdefault = getdefault
        self._required_type = required_type
        self._whitelist = whitelist

        self._values = weakref.WeakKeyDictionary()
        self.changed = signals.Signal(name + '.changed')

    def __repr__(self):
        """Return a string representation of the property."""
        return '<BananaGUI property %r>' % self._name

    def copy(self):
        """Return a copy of self."""
        result = type(self)()
        for attribute in ('_converter', '_allow_none', '_default',
                          '_getdefault', '_required_type', '_whitelist'):
            setattr(result, attribute, getattr(self, attribute))
        return result

    def converter(self, new_converter):
        """Change the converter and return self.

        Use this as a decorator.
        """
        self._converter = new_converter
        return self

    def raw_set(self, instance, value):
        """Set the value directly to the cache and emit the changed signal."""
        self._values[instance] = value
        self.changed.emit(instance)

    def set(self, instance, value):
        """Set the value and emit the changed signal.

        Setting a property's value works like this:
          - Make sure the instance's type has a setter. If this
            property's name is NAME and the instance's type is
            TYPE, the setter is TYPE._bananagui_set_NAME.
          - If allow_none is false, make sure the value is not None.
          - If converter is not None and the value is not None, pass
            the value through converter.
          - Make sure the converted value is an instance of
            required_type.
          - If whitelist is not None, make sure the converted value is
            in the whitelist.
          - Get the current value. If it's equal to the new value, stop
            the setting process.
          - Call the setter with the instance and the converted value
            as arguments.
          - Set the value to the cache.
        """
        setter = getattr(type(instance), '_bananagui_set_'+self._name, None)
        if setter is None:
            raise exceptions.NotSettable(self._name)

        if value is None:
            # Bypass the converting, type checking and whitelist
            # checking.
            if not self._allow_none:
                raise ValueError("None is not allowed")
        else:
            value = self._converter(value)
            if not isinstance(value, self._required_type):
                raise TypeError("expected %s, got %r"
                                % (self._required_type.__name__, value))
            if self._whitelist is not None and value not in self._whitelist:
                raise ValueError("%r is not allowed" % (value,))

        if self.get(instance) != value:
            setter(instance, value)
            self.raw_set(instance, value)

    def raw_get(self, instance):
        """Get the value directly from the cache."""
        if self._default is not _NOTHING:
            return self._values.setdefault(instance, self._default)
        if self._getdefault is not None:
            return self._values.setdefault(instance, self._getdefault())
        # No defaults can be used, raise a KeyError if the value hasn't
        # been set.
        return self._values[instance]

    def get(self, instance):
        """Get the value.

        Getting works like this:
          - If the instance's type doesn't have a getter, return the
            value from the cache. If this property's name is NAME and
            the instance's type is TYPE, the getter is
            TYPE._bananagui_get_NAME.
          - If the value is not in the cache and default or getdefault
            is set, use it to get the value. Note that the getdefault
            function will be called with the instance as an argument.
          - If a getter is defined, call it with the instance as the
            only argument and return the result.
        """
        getter = getattr(type(instance), 
                         '_bananagui_get_' + self._name,
                         self.raw_get)
        return getter(instance)
