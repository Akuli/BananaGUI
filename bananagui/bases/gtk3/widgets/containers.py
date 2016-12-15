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
from .basewidgets import Child, Widget


class Bin(Widget):

    def add(self, child):
        self.real_widget.add(child.real_widget)
        # If this is a GtkScrolledWindow and child doesn't support
        # scrolling, adding the child creates a GtkViewPort and adds it
        # to this widget instead. We can't use child.real_widget.show
        # here because that wouldn't show the viewport. We also can't
        # do self.real_widget.show_all() because that would unhide
        # Window and Dialog widgets.
        self.real_widget.get_child().show_all()

    def remove(self, child):
        # The child isn't necessary the widget in this widget as
        # explained above.
        self.real_widget.remove(self.real_widget.get_child())


_expand_indexes = {
    bananagui.HORIZONTAL: 0,
    bananagui.VERTICAL: 1,
}


class Box(Child):

    def __init__(self, bananawidget, parent, orientation):
        self.real_widget = Gtk.Box(orientation=orientations[orientation])
        super().__init__(bananawidget, parent)

    def append(self, child):
        # TODO: What if the widget is added and then its expandiness is
        # changed?
        expandindex = _expand_indexes[self.bananawidget.orientation]
        expand = child.bananawidget.expand[expandindex]
        self.real_widget.pack_start(child.real_widget, expand, expand, 0)
        child.real_widget.show()

    def remove(self, child):
        self.real_widget.remove(child.real_widget)


class Scroller(Child, Bin):

    def __init__(self, bananawidget, parent):
        self.real_widget = Gtk.ScrolledWindow()
        super().__init__(bananawidget, parent)
