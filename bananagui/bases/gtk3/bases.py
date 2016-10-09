from gi.repository import Gtk


class Widget:

    def _bananagui_set_tooltip(self, tooltip):
        self['real_widget'].set_tooltip_text(tooltip)

    def _bananagui_set_background(self, background):
        


class Parent:
    pass


class Child:

    def _bananagui_set_expand(self, expand):
        horizontal, vertical = expand
        self['real_widget'].set_hexpand(horizontal)
        self['real_widget'].set_vexpand(vertical)

    def _bananagui_set_grayed_out(self, grayed_out):
        self['real_widget'].set_sensitive(not grayed_out)


class Dummy:

    def __init__(self, parent, **kwargs):
        self.real_widget.raw_set(Gtk.Label())
        super().__init__(parent, **kwargs)
