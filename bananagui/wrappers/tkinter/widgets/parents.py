import tkinter as tk

from bananagui import Orient
from . import tkinter_fills
from .basewidgets import Child, Widget, run_when_ready


class Parent(Widget):

    def __init__(self, bananawidget):
        # This is for compatibility with run_when_ready().
        if not hasattr(self, 'parent'):
            self.parent = None
        super().__init__(bananawidget)

    def create(self, parent):
        # self can be a Child, and there's no guarantees about which
        # order Parent and Child appear in the mro. Window and Dialog
        # objects also have this method, but it's never called.
        if hasattr(super(), 'create'):
            # It's a Child, not a Window or Dialog.
            assert parent is not None
            super().create(parent)
        for child in self.bananawidget.children():
            child._wrapper.create(self)

    def _prepare_add(self, child):
        """Prepare a child for being added to this widget."""
        child._packed = True
        if child.widget is None:
            child.create(self)

    def _prepare_remove(self, child):
        """Prepare a child for being removed from this widget."""
        child._packed = False


class Bin(Parent):

    # The _real_add is used in window.py.
    def _real_add(self, child):
        self._prepare_add(child)
        child.widget.pack()
        child.set_expand(child.bananawidget.expand)  # Update the packing.

    add = run_when_ready(_real_add)

    @run_when_ready
    def remove(self, child):
        self._prepare_remove(child)
        child.widget.pack_forget()


# TODO: Scroller.


_appendsides = {
    # Appending to a box adds a child to the beginning of the box, and
    # then the next child towards the center from the first child and
    # so on.
    Orient.HORIZONTAL: 'left',
    Orient.VERTICAL: 'top',
}


class Box(Parent, Child):

    def __init__(self, bananawidget, orient):
        self.orient = orient
        super().__init__(bananawidget)

    def create_widget(self, parent):
        return tk.Frame(parent.widget)

    @run_when_ready
    def append(self, child):
        self._prepare_add(child)
        child.widget.pack(
            side=_appendsides[self.bananawidget.orient],
            fill=tkinter_fills[child.bananawidget.expand],
        )
        # Make pack expand it correctly.
        child.set_expand(child.bananawidget.expand)

    @run_when_ready
    def remove(self, child):
        self._prepare_remove(child)
        child.widget.pack_forget()


class Group(Bin, Child):

    def create_widget(self, parent):
        return tk.LabelFrame(parent.widget)

    @run_when_ready
    def set_text(self, text):
        self.widget['text'] = text
