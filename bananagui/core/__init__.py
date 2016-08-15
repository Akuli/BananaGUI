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

import weakref

from . import bases, buttons, labels, layouts, windows

# Allow None as a non-default value.
NOTHING = object()


# Signal, Property and ObjectBase
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Signal:
    """A signal that contains callbacks and can be emitted."""

    def __init__(self):
        """Initialize a signal."""
        self._callbacks = weakref.WeakKeyDictionary()

    def copy(self):
        """Return a copy of self."""
        if self._callbacks:
            raise ValueError("cannot copy a signal after adding callbacks")
        return type(self)()

    def set(self, instance, callback_list):
        """Set the callbacks list."""
        self._callbacks.setdefault(instance, [])
        if self._callbacks[instance] is not callback_list:
            if not isinstance(callback_list, list):
                callback_list = list(callback_list)
            self._callbacks[instance] = callback_list

    def get(self, instance):
        """Return the callback list.

        The list can be modified, but it may be replaced with a new list
        later.
        """
        return self._callbacks[instance]

    def emit(self, instance, *args):
        """Call the callbacks with args."""
        for callback in self.get_callback_list(instance):
            callback(*args)


class Property:
    """A basic property.

    The properties are not like Python properties. They are more like
    properties in large GUI toolkits like Qt and GTK+.

    Setting a property's value works like this:
      - Make sure setter is not None.
      - If allow_none is false, make sure the value is not None.
      - If converter is not None and the value is not None, pass the
        value through converter.
      - Make sure the converted value is an instance of required_type.
      - If whitelist is not None, make sure the converted value is in
        the whitelist.
      - Get the current value. If it's equal to the new value, stop the
        setting process.
      - Call the setter with the instance and the converted value as
        arguments.
      - Set the value to a cache.

    Getting works like this:
      - If no getter has been set, return the value from the cache. If
        the value is not in the cache and default or getdefault is set,
        use it to get the value. Note that the getdefault function will
        be called with the BaseObject instance as an argument.
      - If a getter has been set, call it with the instance as the only
        argument and return the result.
    """

    def __init__(self, *,
                 converter=lambda x: x,
                 allow_none=False,
                 default=_NOTHING,
                 getdefault=None,
                 required_type=object,
                 whitelist=None,
                 setter=None,
                 getter=None):
        """Initialize the property.

        See the class docstring for explanations about the arguments.
        """
        if default is not _NOTHING and getdefault is not None:
            raise ValueError("specify default or getdefault, not both")
        self._converter = converter
        self._allow_none = allow_none
        self._default = default
        self._getdefault = getdefault
        self._required_type = required_type
        self._whitelist = whitelist
        self._setter = setter
        self._getter = getter

        self._values = weakref.WeakKeyDictionary()
        self.changed = Signal()

    def copy(self):
        """Return a copy of self."""
        if self._values:
            raise ValueError("cannot copy an attribute after adding values")
        result = type(self)()
        for attribute in ('_converter', '_allow_none', '_default',
                          '_getdefault', '_required_type', '_whitelist',
                          '_setter', '_getter'):
            setattr(result, attribute, getattr(self, attribute))
        return result

    def setter(self, new_setter):
        """Change the setter and return self.

        Use this as a decorator.
        """
        self._setter = new_setter
        return self

    def getter(self, new_getter):
        """Change the getter and return self.

        Use this as a decorator.
        """
        self._getter = new_getter
        return self

    def converter(self, new_converter):
        """Change the converter and return self.

        Use this as a decorator.
        """
        self._converter = new_converter
        return self

    def raw_set(self, instance, value):
        """Set the value directly to the cache and emit the changed signal."""
        self._values[instance] = value
        self.changed.emit(value)

    def set(self, instance, value):
        """Set the value and emit the changed signal."""
        if self._setter is None:
            raise ValueError("cannot set the value")
        if value is None and not self._allow_none:
            raise ValueError("None is not allowed")
        value = self._converter(value)
        if not isinstance(value, self.required_type):
            raise TypeError("expected %s, got %r"
                            % (self._required_type.__name__, value))
        if self.whitelist is not None and value not in self._whitelist:
            raise ValueError("%r is not allowed" % (value,))
        if self.get(instance) != value:
            self._setter(instance, value)
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
        """Get the value."""
        if self._getter is None:
            return self.raw_get(instance)
        return self._getter(instance)

    @classmethod
    def nonnegative(cls, **kwargs):
        """Create a Property that does not accept negative values."""
        old_converter = kwargs.pop('converter', lambda x: x)

        def converter(value):
            value = old_converter(value)
            if value < 0:
                raise ValueError("%r is negative" % (value,))
            return value

        return cls(**kwargs, converter=converter)

    @classmethod
    def alias(cls, propertyname):
        """Create a property that calls the other property on set and get.

        The returned property has customized setter and getter, so it's
        not recommended to replace them.
        """
        def setter(self, value):
            self[propertyname] = value

        def getter(self, value):
            return self[propertyname]

        return cls(setter=setter, getter=getter)

    @classmethod
    def tuplealias(cls, *propertynames):
        """A tuple of other Properties.

        propertynames should be other properties' names. The returned
        property has customized converter, setter and getter, so it's
        not recommended to replace them.
        """
        def setter(self, valuetuple):
            if len(propertynames) != len(valuetuple):
                raise ValueError("expected length %d, got %d"
                                 % (len(propertynames), len(valuetuple)))
            for name, value in zip(propertynames, valuetuple):
                self[name] = value

        def getter(self):
            return tuple(self[name] for name in propertynames)

        return cls(converter=tuple, setter=setter, getter=getter)


class ObjectBase:
    """An object that allows using properties and signals with subscripting.

    To access a changed signal of a property, you can subscript with
    'propertyname.changed'.
    """

    def __prop_or_sig(self, propertyname_or_signalname):
        property_or_signal = type(self)
        for attribute in propertyname_or_signalname.split('.'):
            property_or_signal = getattr(property_or_signal, attribute)
        if not isinstance(property_or_signal, (Property, Signal)):
            raise TypeError("expected a Property or a Signal, got %r"
                            % (property_or_signal,))
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


# Module-level functions
# ~~~~~~~~~~~~~~~~~~~~~~

def init():
    """Initialize BananaGUI.

    Call this before calling anything else.
    """


def main():
    """Run the mainloop until quit() is called.

    This returns an exit status if the wrapped GUI toolkit supports it,
    so you can do something like sys.exit(yourwrapper.main())
    """


def quit():
    """Quit the mainloop."""


# 
