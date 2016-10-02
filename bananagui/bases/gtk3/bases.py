from gi.repository import Gtk


class WidgetBase:
    pass


class ParentBase:
    pass


class ChildBase:

    def _bananagui_set_tooltip(self, tooltip):
        self['real_widget'].set_tooltip_text(tooltip)

    def _bananagui_set_grayed_out(grayed_out):
        self['real_widget'].set_sensitive(not grayed_out)


class BinBase:

    def _bananagui_set_child(self, child):
        if self['child'] is not None:
            self['real_widget'].remove(self['child']['real_widget'])
        if child is not None:
            self['real_widget'].add(child['real_widget'])
