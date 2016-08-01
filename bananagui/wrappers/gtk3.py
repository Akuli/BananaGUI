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
