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

from gi.repository import Gtk, GLib


class Progressbar:

    def __init__(self, parent, **kwargs):
        self.real_widget = Gtk.ProgressBar()
        super().__init__(parent, **kwargs)

    def _set_progress(self, progress):
        self.real_widget.set_fraction(progress)


class BouncingProgressbar:

    def __init__(self, parent, **kwargs):
        widget = Gtk.ProgressBar(orientation=Gtk.Orientation.HORIZONTAL)
        self.real_widget = widget
        super().__init__(parent, **kwargs)

    def _on_timeout(self):
        if not self.bouncing:
            return False
        self.real_widget.pulse()
        return True  # Run this again.

    def _set_bouncing(self, bouncing):
        if bouncing:
            GLib.timeout_add(100, self._on_timeout)
        else:
            # The _on_timeout method knows when to stop, but we need to
            # move the progressbar back to the beginning now.
            self.real_widget.set_fraction(0)


class Spinner:

    def __init__(self, parent, **kwargs):
        self.real_widget = Gtk.Spinner()
        super().__init__(parent, **kwargs)

    def _set_spinning(self, spinning):
        if spinning:
            self.real_widget.start()
        else:
            self.real_widget.stop()
