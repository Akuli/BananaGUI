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

import functools

import bananagui


class Signal:
    """A signal that calls its callbacks when it's emitted.

    The callbacks are internally stored in a list, and when the signal
    is emitted, each callback in the is called in the order they are in
    the list. Adding a callback appends to the list, and removing a
    callback removes the first occurance in the list.
    """

    def __init__(self):
        """Initialize a signal with no callbacks."""
        self._callbacks = []

    def connect(self, callback):
        """Add a callback.

        If the same callback is added twice, it will be called twice.
        """
        if not callable(callback):
            raise TypeError("callbacks must be callable")
        self._callbacks.append(callback)

    def is_connected(self, callback):
        """Check if a callback has been added."""
        return callback in self._callbacks

    def disconnect(self, callback):
        """Remove a callback.

        If a callback is added twice, the first occurance will be
        removed.
        """
        self._callbacks.remove(callback)

    def emit(self, *args):
        """Call the callbacks with args."""
        for callback in self._callbacks:
            callback(*args)


class Property:
    """Container for a setter, a getter and a changed signal."""

    def __init__(self, setter=None, getter=None):
        """Initialize the Property."""
        self._setter = setter
        self._getter = getter
        self.changed = Signal()

    def set(self, value):
        """Set the property's value.

        Raise a PropertyError if the value cannot be set.
        """
        if self._setter is None:
            raise bananagui.PropertyError("cannot set the value")
        self._setter(value)

    def get(self):
        """Return the property's current value.

        Raise a PropertyError if the value cannot be retrieved.
        """
        if self._getter is None:
            raise bananagui.PropertyError("cannot get the value")
        return self._getter()

    def emit_changed(self):
        """Emit the changed signal with the current value.

        The getter should call this when changing the value succeeds.
        """
        self.changed.emit(self._getter())


class _BaseObjectMeta(type):
    """A metaclass for BaseObject."""

    def __new__(metaclass, name, bases, dictionary):
        """Create and return a new BaseObject subclass."""
        new_signals = dictionary.pop('signals', [])
        new_properties = dictionary.pop('properties', [])
        cls = super().__new__(metaclass, name, bases, dictionary)

        cls.signals = getattr(cls, 'signals', []) + new_signals
        cls.properties = getattr(cls, 'properties', []) + new_properties
        return cls


class BaseObject(metaclass=_BaseObjectMeta):
    """An object that allows using properties with subscripting."""

    signals = []
    properties = []

    def __init__(self):
        """Set up properties and signals."""
        for signame in self.signals:
            setattr(self, signame, Signal())
        for propname in self.properties:
            prop = Property(
                getattr(self, 'set_' + propname, None),
                getattr(self, 'get_' + propname, None),
            )
            setattr(self, propname, prop)

    def __setitem__(self, propname, value):
        """Set a property's value."""
        try:
            prop = getattr(self, propname)
        except AttributeError as e:
            raise bananagui.PropertyError("no such property: {!r}"
                                          .format(propname)) from e
        prop.set(value)

    def __getitem__(self, propname):
        """Return a property's value."""
        try:
            prop = getattr(self, propname)
        except AttributeError as e:
            raise bananagui.PropertyError("no such property: {!r}"
                                          .format(propname)) from e
        return prop.get()
