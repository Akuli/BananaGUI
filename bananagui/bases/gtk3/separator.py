from gi.repository import Gtk

from bananagui import HORIZONTAL, VERTICAL


_orientations = {
    HORIZONTAL: Gtk.Orientation.HORIZONTAL,
    VERTICAL: Gtk.Orientation.VERTICAL,
}


class Separator:

    def __init__(self, parent, **kwargs):
        gtk_orientation = _orientations[self['orientation']]
        widget = Gtk.Separator(orientation=gtk_orientation)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)
