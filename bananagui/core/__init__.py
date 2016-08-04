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


class Signal:
    """A signal."""

    def __init__(self):
        """Initialize a signal with no callbacks."""
        self._callbacks = []

    def connect(self, callback):
        """Add a callback."""
        if not callable(callback):
            raise ValueError("callbacks must be callable")
        self._callbacks.append(callback)

    def is_connected(self, callback):
        """Check if callback has been added."""
        return callback in self._callbacks

    def disconnect(self, callback):
        """Remove a callback."""
        self._callbacks.remove(callback)

    def emit(self, *args):
        """Call the callbacks with args."""
        for callback in self._callbacks:
            callback(*args)


class Property:
    """A Property.

    The Properties are more like properties in GUI toolkits like PyQt
    and GTK+ than Python properties. When the value of the property is
    changed with set(), its changed signal will be emitted with the new
    value.
    """

    # The properties are called explicitly instead of using __set__ and
    # __get__ to avoid interference with other attributes in subclasses,
    # e.g. label.text = 'hello' overwrites the property instead of
    # changing its value with descriptor magic. label.text.set('hello')
    # or label['text'] = 'hello' would change the value.

    def __init__(self, default_value):
        """Initialize the Property."""
        self._setter = None
        self._getter = None
        self._value = default_value
        self.changed = Signal()

    def set(self, value):
        """Set the Property's value and emit the callback signal."""
        if self._setter is None:
            raise ValueError("cannot set the value")
        self._setter(value)
        self._value = value
        self.changed.emit(value)

    def get(self):
        """Return the current value."""
        if self._getter is None:
            return self._value
        return self._getter()

    def emit_changed(self):
        """Emit the changed signal.

        This is equivalent to self.changed.emit(self.get()).
        """
        self.changed.emit(self.get())


class BaseObject:
    """An object that allows using properties with subscripting."""

    def __setitem__(self, propname, value):
        """Set a property's value."""
        try:
            prop = getattr(self, propname)
        except AttributeError as e:
            raise KeyError(propname) from e
        prop.set(value)

    def __getitem__(self, propname):
        """Return a property's value."""
        try:
            prop = getattr(self, propname)
        except AttributeError as e:
            raise KeyError(propname) from e
        return prop.get()
