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

"""This module contains property classes.

This is in a separate file because there are many property classes.
"""

import collections
import functools
import weakref

from bananagui.core import signals


class Anything:
    """A basic property.

    The properties are not like Python properties. They are more like
    properties in large GUI toolkits like Qt and GTK+.
    """

    # This is used for converting the value. By default, this returns
    # the value unchanged default, but subclasses may override this.

    def __init__(self, allow_none, get_default=None):
        """Initialize the property.

        Note that if get_default is not None it must be callable. It's
        called without any arguments to get a default value.

        If allow_none is True, None will be allowed as the value.
        The _allow_none attribute is set to allow_none.
        """
        self._setter = None
        self._getter = None
        self._get_default = get_default
        self._allow_none = allow_none
        self._values = weakref.WeakKeyDictionary()
        self.changed = signals.Signal()

    def setter(self, setter):
        """Change the setter and return self.

        Use this as a decorator.
        """
        self._setter = setter
        return self

    def getter(self, getter):
        """Change the getter and return self.

        If the getter returns NotImplemented, the value that was set
        last time will be used. Use this as a decorator.
        """
        self._getter = getter
        return self

    def raw_set(self, instance, value):
        """Set the value directly to the cache."""
        self._values[instance] = value

    def set(self, instance, value):
        """Set the value.

        Also emit the changed signal if the old value and new value are
        not equal.
        """
        if self._setter is None:
            raise bananagui.ReadOnlyPropertyError("cannot set the value")
        if value is None and not self._allow_none:
            raise ValueError("None is not allowed")
        value = self._convert(instance, value)
        old_value = self.raw_get(instance)
        self._setter(instance, value)
        self.raw_set(instance, value)
        if old_value != value:
            self.changed.emit(value)

    def raw_get(self, instance):
        """Get the value directly from the cache."""
        return self._values[instance]

    def get(self, instance):
        """Get the value."""
        if self._getter is None:
            return self.raw_get(instance)
        return self._getter(instance)

    def _convert(self, instance, value):
        """Convert the value.

        This returns the value unchanged default. Subclasses may
        override this, but they should call super() to support multiple
        inheritance.
        """
        return value


class Integer(Anything):
    """A property that converts its value to an integer."""

    def _convert(self, instance, value):
        return int(value)


class Boolean(Anything):
    """A property that converts its value to a Boolean."""

    def _convert(self, instance, value):
        return bool(value)


class String(Anything):
    """A property that converts its values to strings."""

    def _convert(self, instance, value):
        return str(value)


class Tuple(Anything):
    """A property that converts its value to a tuple."""

    def __init__(self, properties, convert, **kwargs):
        """Initialize the property.

        The properties argument should be a tuple of other properties
        this property contains.
        """
        self._properties = tuple(properties)
        super().__init__(**kwargs)

    def _convert(self, instance, value):
        for prop, item in zip(self.properties, value):
            prop.set(instance, value)
        # raw_get can be used, because the value was just set.
        value = tuple(prop.raw_get(instance) for prop in self._properties)
        return super()._convert(value)


class IsInstance(Anything):
    """A property that checks the type of its value with isinstance."""

    def __init__(self, required_type):
        """Initialize the property.

        The values will be checked with isinstance(value, required_type).
        """
        self._type = required_type

    @functools.wraps(Anything.set)
    def set(self, instance, value):
        if not isinstance(value, self._type):
            raise TypeError("expected %s, got %r"
                            % (self._type.__name__, value))


class WhiteListed(Anything):
    """A property that only allows values that are in a whitelist."""

    def __init__(self, whitelist, **kwargs):
        super().__init__(**kwargs)
        self._whitelist = whitelist

    def _convert(self, instance, value):
        if value not in self._whitelist:
            raise ValueError("%r is not in the whitelist" % (value,))
        return super()._convert(value)


class WhiteListedInteger:
    
