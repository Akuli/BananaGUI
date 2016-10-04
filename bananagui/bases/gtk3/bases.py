from gi.repository import Gtk


class WidgetBase:
    pass


class ParentBase:
    pass


class ChildBase:

    def _bananagui_set_expand(self, expand):
        h, v = expand
        self['real_widget'].set_hexpand(horizontal)
        self['real_widget'].set_vexpand(vertical)

    def _bananagui_set_tooltip(self, tooltip):
        self['real_widget'].set_tooltip_text(tooltip)

    def _bananagui_set_grayed_out(grayed_out):
        self['real_widget'].set_sensitive(not grayed_out)


class Dummy:

    def __init__(self, parent):
        #super().__init__(parent)
        raise NotImplementedError  # TODO
