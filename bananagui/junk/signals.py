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

"""BananaGUI events and signals."""

import contextlib
import weakref

from bananagui import properties


class Event:
    """A simple container class."""

    def __init__(self, widget, **kwargs):
        self.widget = widget
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __repr__(self):
        words = ['BananaGUI', 'event']
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                words.append('%s=%r' % (name, value))
        return '<%s>' % ' '.join(words)


class Signal(properties.Property):
    """A signal that contains callbacks and can be emitted."""

    def __init__(self, name):
        """Initialize a signal."""
        super().__init__(name, getdefault=list, required_type=list,
                         add_changed=False)
        self._blocked = weakref.WeakSet()

    def emit(self, widget, **kwargs):
        """Call the callbacks with an event created from arguments."""
        if widget not in self._blocked:
            event = Event(widget, **kwargs)
            for callback in self.get(widget):
                callback(event)

    @contextlib.contextmanager
    def blocked(self, widget):
        """Block the signal from emitting temporarily.

        Blocking is widget-specific. Use this as a context manager.
        """
        self._blocked.add(widget)
        try:
            yield
        finally:
            self._blocked.remove(widget)
