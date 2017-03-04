from gi.repository import Gtk, GLib

from .basewidgets import Child


class Progressbar(Child):

    def __init__(self, bananawidget):
        self.widget = Gtk.ProgressBar()
        super().__init__(bananawidget)

    def set_progress(self, progress):
        self.widget.set_fraction(progress)


class BouncingProgressbar(Child):

    def __init__(self, bananawidget):
        self.widget = Gtk.ProgressBar()
        super().__init__(bananawidget)

    def _on_timeout(self):
        if not self._bouncing:
            return False  # Stop this.
        self.widget.pulse()
        return True     # Run this again.

    def set_bouncing(self, bouncing):
        self._bouncing = bouncing
        if bouncing:
            GLib.timeout_add(100, self._on_timeout)
        else:
            # The _on_timeout method knows when to stop, but we need to
            # move the progressbar back to the beginning now.
            self.widget.set_fraction(0)
