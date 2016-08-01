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

"""GTK+ 3 wrapper for BananaGUI."""

import functools

import gi
gi.require_version('Gtk', '3.0')    # noqa
from gi.repository import Gtk

from gui.core import widgets


class Widget(widgets.Widget):

    __doc__ = widgets.Widget.__doc__

    @functools.wraps(widgets.Widget.__init__)
    def __init__(self):
        super().__init__()
        self.tooltip._setter = self.__set_tooltip
        self.size._getter = self.__get_size

    def __set_tooltip(self, tooltip):
        self.real_widget().set_tooltip_text(tooltip)

    def __del__(self):
        """Destroy the widget to free up any resources used by it."""
        if self.real_widget() is not None:
            self.real_widget().destroy()


class Parent(widgets.Parent, Widget):

    __doc__ = widgets.Parent.__doc__


class Bin(widgets.Bin, Parent):

    __doc__ = widgets.Bin.__doc__

    @functools.wraps(widgets.Bin.__init__)
    def __init__(self):
        super().__init__()
        self.child._setter = self.__set_child

    def __set_child(self, child):
        # Check if the child is already in the bin.
        if child is self.child():
            return
        # Remove the old child if it's set.
        if self.child() is not None:
            self.real_widget().remove(self.child().real_widget())
        # Check the new child and add it.
        if child is not None:
            if child.parent() is not self:
                raise ValueError("cannot add a child with the wrong parent")
            self.real_widget().add(child)
        # Change the property's value.
        with self.child._run_callbacks():
            self.child._value = child

    def __set_grayed_out(self, grayed_out):
        self.real_widget().set_sensitive(not grayed_out)
