from gi.repository import Gtk


class BoxBase:

    def __init__(self, parent):
        super().__init__(parent)
        widget = Gtk.Box(orientation=type(self)._bananagui_gtk_orientation)
        self.raw_set('real_widget', widget)

    def add_start(self, child, expand):
        self['real_widget'].pack_start(child['real_widget'], expand, expand, 0)

    def add_end(self, child, expand):
        self['real_widget'].pack_end(child['real_widget'], expand, expand, 0)

    def remove(self, child):
        self['real_widget'].remove(child['real_widget'])


class HBox:
    _bananagui_gtk_orientation = Gtk.Orientation.HORIZONTAL


class VBox:
    _bananagui_gtk_orientation = Gtk.Orientation.VERTICAL
