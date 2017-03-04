from gi.repository import Gtk

from . import orientations
from .basewidgets import Child


class Checkbox(Child):

    def __init__(self, bananawidget):
        self.widget = Gtk.CheckButton()
        self.widget.connect('notify::active', self._do_check)
        super().__init__(bananawidget)

    def _do_check(self, widget, gparam):
        self.bananawidget.checked = widget.get_active()

    def set_text(self, text):
        self.widget.set_label(text)

    def set_checked(self, checked):
        self.widget.set_active(checked)


class Dummy(Child):

    def __init__(self, bananawidget):
        self.widget = Gtk.Label()
        super().__init__(bananawidget)


class Separator(Child):

    def __init__(self, bananawidget, orientation):
        gtk_orientation = orientations[orientation]
        self.widget = Gtk.Separator(orientation=gtk_orientation)
        super().__init__(bananawidget)
