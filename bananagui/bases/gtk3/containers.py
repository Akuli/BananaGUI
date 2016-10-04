from gi.repository import Gtk


class ParentBase:
    pass


class BinBase:

    def _bananagui_set_child(self, child):
        if self['child'] is not None:
            self['real_widget'].remove(self['child']['real_widget'])
        if child is not None:
            self['real_widget'].add(child['real_widget'])


class BoxBase:

    def __init__(self, parent):
        super().__init__(parent)
        widget = Gtk.Box(orientation=type(self)._bananagui_gtk_orientation)
        self.real_widget.raw_set(widget)

    def append(self, child):
        # TODO: What if the widget is added and then its expandiness is
        # changed? How about a custom BoxBase subclass that is not a
        # HBox or a VBox?
        expand = child['expand'][self._bananagui_gtk_expandindex]
        self['real_widget'].pack_start(child['real_widget'], expand, expand, 0)

    def remove(self, child):
        self['real_widget'].remove(child['real_widget'])


class HBox:
    _bananagui_gtk_orientation = Gtk.Orientation.HORIZONTAL
    _bananagui_gtk_expandindex = 0


class VBox:
    _bananagui_gtk_orientation = Gtk.Orientation.VERTICAL
    _bananagui_gtk_expandindex = 1
