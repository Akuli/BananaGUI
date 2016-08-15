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

"""This module contains the signal class.

This is in a separate file to avoid circular imports.
"""

import collections


class Signal:
    """A signal that contains callbacks and can be emitted."""

    def __init__(self):
        """Initialize a signal."""
        self._callbacks = collections.defaultdict(list)

    def set(self, instance, callback_list):
        """Set the callbacks list."""
        if self._callbacks[id(instance)] is not callback_list:
            if not isinstance(callback_list, list):
                callback_list = list(callback_list)
            self._callbacks[id(instance)] = callback_list

    def get(self, instance):
        """Return the callback list.

        The list can be modified, but it may be replaced with a new list
        later.
        """
        return self._callbacks[id(instance)]

    def emit(self, instance, *args):
        """Call the callbacks with args."""
        for callback in self.get_callback_list(instance):
            callback(*args)
