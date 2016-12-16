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

import ctypes

import bananagui
from .libs import gtk
from .textwidgets import TextEdit


class Bin:

    def _set_child(self, child):
        # The old child isn't necessarily self.child.real_widget. See
        # Scroller.
        print('_set_child', self, child)
        old_child = gtk.gtk_bin_get_child(self.real_widget)
        if old_child is not None:
            print('_set_child: removing child', old_child)
            gtk.gtk_container_remove(self.real_widget, old_child)
        if child is not None:
            print('_set_child: adding child', child)
            gtk.gtk_container_add(self.real_widget, child.real_widget)
            gtk.gtk_widget_show(child.real_widget)


_expand_indexes = {
    bananagui.HORIZONTAL: 0,
    bananagui.VERTICAL: 1,
}


class Box:

    def __init__(self, parent, **kwargs):
        if self.orientation == bananagui.HORIZONTAL:
            new = gtk.gtk_hbox_new
        if self.orientation == bananagui.VERTICAL:
            new = gtk.gtk_vbox_new
        self.real_widget = new(False, 0)
        super().__init__(parent, **kwargs)

    def _append(self, child):
        # TODO: what if the widget is added and then its expandiness is
        # changed?
        expandindex = _expand_indexes[self.orientation]
        expand = child.expand[expandindex]
        gtk.gtk_box_pack_start(self.real_widget, child.real_widget,
                               expand, expand, 0)
        gtk.gtk_widget_show(child.real_widget)

    def _remove(self, child):
        gtk.gtk_container_remove(self.real_widget, child.real_widget)


def _create_adjustment():
    """Create a GtkAdjustment for Scroller.

    This sets everything to same default values as GTK+ 3 in gi.repository.
    """
    args = [0.0] * 6
    return gtk.gtk_adjustment_new(*args)


class Scroller:

    def __init__(self, parent, **kwargs):
        self.real_widget = gtk.gtk_scrolled_window_new(
            _create_adjustment(), _create_adjustment())

    def _set_child(self, child):
        supports_scrolling = (TextEdit,)
        if child is None or isinstance(child, supports_scrolling):
            # We can add or remove it normally.
            super()._set_child(child)
        else:
            # We need a ViewPort.
            super()._set_child(None)    # Remove old child if any.
            gtk.gtk_scrolled_window_add_with_viewport(
                self.real_widget, child.real_widget)
            viewport = gtk.gtk_bin_get_child(self.real_widget)
            gtk.gtk_widget_show_all(viewport)  # Show viewport and child.
