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

from gi.repository import Gtk

import bananagui
from . import orientations


class Bin:

    def _set_child(self, child):
        # The widget in self.real_widget can be something else than
        # self.child.real_widget. See Scroller.
        old_child = self.real_widget.get_child()
        if old_child is not None:
            self.real_widget.remove(old_child)
        if child is not None:
            self.real_widget.add(child.real_widget)
            child.real_widget.show()


_expand_indexes = {
    bananagui.HORIZONTAL: 0,
    bananagui.VERTICAL: 1,
}


class Box:

    def __init__(self, parent, **kwargs):
        gtk_orientation = orientations[self.orientation]
        self.real_widget = Gtk.Box(orientation=gtk_orientation)
        super().__init__(parent, **kwargs)

    def _append(self, child):
        # TODO: What if the widget is added and then its expandiness is
        # changed?
        expandindex = _expand_indexes[self.orientation]
        expand = child.expand[expandindex]
        self.real_widget.pack_start(child.real_widget, expand, expand, 0)
        child.real_widget.show()

    def _remove(self, child):
        self.real_widget.remove(child.real_widget)


class Scroller:

    def __init__(self, parent, **kwargs):
        self.real_widget = Gtk.ScrolledWindow()
        super().__init__(parent, **kwargs)

    def _set_child(self, child):
        if child is None or isinstance(child, Gtk.Scrollable):
            # We can add or remove it normally.
            super()._set_child(child)
        else:
            # We need to add it with a ViewPort.
            super()._set_child(None)     # Remove the old child if any.
            self.real_widget.add_with_viewport(child.real_widget)
            self.real_widget.get_child().show_all()  # Show viewport and child.
