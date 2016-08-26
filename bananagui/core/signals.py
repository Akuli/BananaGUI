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

"""Simple signal class for BananaGUI."""

import weakref


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
        return type(self)()

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
