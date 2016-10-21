from gi.repository import Gtk

import bananagui
from . import orientations


class Bin:

    def _bananagui_set_child(self, child):
        if self['child'] is not None:
            self['real_widget'].remove(self['child']['real_widget'])
        if child is not None:
            self['real_widget'].add(child['real_widget'])
            child['real_widget'].show()


_expand_indexes = {
    bananagui.HORIZONTAL: 0,
    bananagui.VERTICAL: 1,
}


class Box:

    def __init__(self, parent, **kwargs):
        gtk_orientation = orientations[self['orientation']]
        widget = Gtk.Box(orientation=gtk_orientation)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def _bananagui_box_append(self, child):
        # TODO: What if the widget is added and then its expandiness is
        # changed?
        expandindex = _expand_indexes[self['orientation']]
        expand = child['expand'][expandindex]
        self['real_widget'].pack_start(child['real_widget'], expand, expand, 0)
        child['real_widget'].show()

    def _bananagui_box_remove(self, child):
        self['real_widget'].remove(child['real_widget'])
