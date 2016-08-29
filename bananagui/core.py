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
import functools
import itertools
import types
import weakref

from bananagui import exceptions

# Allow None as a non-default value.
_NOTHING = object()


# BananaGUI wrapper loader
# ~~~~~~~~~~~~~~~~~~~~~~~~

class WrapperLoader:

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
        for name in set(dir(self._wrappermodule)) - set(dir(self._basemodule)):
            if not name.startswith('_'):
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


# Property
# ~~~~~~~~

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
        self.changed = Signal(name + '.changed')

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


# Signal
# ~~~~~~

class Signal:
    """A signal that contains callbacks and can be emitted."""

    def __init__(self, name):
        """Initialize a signal."""
        self._name = name
        self._callbacks = weakref.WeakKeyDictionary()

    def __repr__(self):
        """Return a string representation of the signal."""
        return '<BananaGUI signal %r>' % self._name

    def copy(self):
        """Return a copy of self."""
        return type(self)(self._name)

    def set(self, instance, callback_list):
        """Set the callbacks list.

        Actually, set the content of the callback list.
        """
        self.get(instance)[:] = callback_list

    def get(self, instance):
        """Return the callback list.

        The list can be mutated or stored in another variable. It is
        never replaced with another list.
        """
        return self._callbacks.setdefault(instance, [])

    def emit(self, instance):
        """Call the callbacks with args."""
        for callback in self.get(instance):
            callback(instance)

    @contextlib.contextmanager
    def blocked(self, instance):
        """Block the signal from emitting temporarily.

        Blocking is instance-specific. Use this as a context manager.
        """
        callbacks = self.get(instance)
        self.set(instance, [])
        try:
            yield
        finally:
            self.set(instance, callbacks)


# ObjectBase
# ~~~~~~~~~~

class ObjectBase:
    """An object that allows using properties and signals with subscripting."""

    def __prop_or_sig(self, name, *, prop=False, sig=False):
        """Get a property or a signal."""
        assert prop or sig, "set prop or sig to a true value"

        result = type(self)
        try:
            for attribute in name.split('.'):
                result = getattr(result, attribute)
        except AttributeError as e:
            raise exceptions.NoSuchPropertyOrSignal(name) from e

        if prop and sig:
            if not isinstance(result, (Property, Signal)):
                raise ValueError("excepted a BananaGUI property or signal, "
                                 "got %r" % (result,))
        elif prop:
            if not isinstance(result, Property):
                raise ValueError("expected a BananaGUI property, got %r"
                                 % (result,))
        elif sig:
            if not isinstance(result, Signal):
                raise ValueError("excepted a BananaGUI signal, got %r"
                                 % (result,))

        return result

    def __setitem__(self, property_or_signal_name, value):
        """Set the value of a property or a signal's callback list."""
        prop_or_sig = self.__prop_or_sig(property_or_signal_name,
                                         prop=True,
                                         sig=True)
        prop_or_sig.set(self, value)

    def __getitem__(self, property_or_signal_name):
        """Return the value of a property or a signal's callback list."""
        prop_or_sig = self.__prop_or_sig(property_or_signal_name,
                                         prop=True,
                                         sig=True)
        return prop_or_sig.get(self)

    def raw_set(self, propertyname, value):
        """Set a property's value directly to its cache."""
        self.__prop_or_sig(propertyname, prop=True).raw_set(self, value)

    def raw_get(self, propertyname):
        """Get a property's value directly from its cache."""
        return self.__prop_or_sig(propertyname, prop=True).raw_get(self)

    def emit(self, signalname):
        """Emit a signal."""
        self.__prop_or_sig(signalname, sig=True).emit(self)

    @contextlib.contextmanager
    def blocked(self, signalname):
        """Block a signal temporarily."""
        with self.__prop_or_sig(signalname, sig=True).blocked(self):
            yield
