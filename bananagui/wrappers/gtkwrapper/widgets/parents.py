# Copyright (c) 2016-2017 Akuli

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

from bananagui import Orient
from . import orientations
from .basewidgets import Child, Widget


class Bin(Widget):

    def add(self, child):
        self.widget.add(child.widget)
        # If this is a GtkScrolledWindow and child doesn't support
        # scrolling, adding the child creates a GtkViewPort and adds it
        # to this widget instead. We can't use child.widget.show
        # here because that wouldn't show the viewport. We also can't
        # do self.widget.show_all() because that would unhide
        # Window and Dialog widgets.
        self.widget.get_child().show_all()

    def remove(self, child):
        # The child isn't necessary the widget in this widget as
        # explained above.
        self.widget.remove(self.widget.get_child())


_expand_indexes = {
    Orient.HORIZONTAL: 0,
    Orient.VERTICAL: 1,
}


class Box(Child):

    def __init__(self, bananawidget, orient):
        self.widget = Gtk.Box(orientation=orientations[orient])
        super().__init__(bananawidget)

    def append(self, child):
        # TODO: What if the widget is added and then its expandiness is
        # changed?
        expandindex = _expand_indexes[self.bananawidget.orient]
        expand = child.bananawidget.expand[expandindex]
        self.widget.pack_start(child.widget, expand, expand, 0)
        child.widget.show()

    def remove(self, child):
        self.widget.remove(child.widget)


class Scroller(Bin, Child):

    def __init__(self, bananawidget):
        self.widget = Gtk.ScrolledWindow()
        super().__init__(bananawidget)


class Group(Bin, Child):

    def __init__(self, bananawidget):
        self.widget = Gtk.Frame()
        super().__init__(bananawidget)

    def set_text(self, text):
        self.widget.set_label(text)
