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

import tkinter as tk

import bananagui
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
        for child in self.bananawidget.iter_children():
            child._wrapper.create(self)

    def _prepare_add(self, child):
        """Prepare a child for being added to this widget."""
        child._packed = True
        if child.real_widget is None:
            child.create(self)

    def _prepare_remove(self, child):
        """Prepare a child for being removed from this widget."""
        child._packed = False


class Bin(Parent):

    # The _real_add is used in window.py.
    def _real_add(self, child):
        self._prepare_add(child)
        child.real_widget.pack()
        child.set_expand(child.bananawidget.expand)  # Update the packing.

    add = run_when_ready(_real_add)

    @run_when_ready
    def remove(self, child):
        self._prepare_remove(child)
        child.real_widget.pack_forget()


# TODO: Scroller.


_appendsides = {
    # Appending to a box adds a child to the beginning of the box, and
    # then the next child towards the center from the first child and
    # so on.
    bananagui.HORIZONTAL: 'left',
    bananagui.VERTICAL: 'top',
}


class Box(Parent, Child):

    def __init__(self, bananawidget, orient):
        self.orient = orient
        super().__init__(bananawidget)

    def create_widget(self, parent):
        return tk.Frame(parent.real_widget)

    @run_when_ready
    def append(self, child):
        self._prepare_add(child)
        child.real_widget.pack(
            side=_appendsides[self.bananawidget.orient],
            fill=tkinter_fills[child.bananawidget.expand],
        )
        # Make pack expand it correctly.
        child.set_expand(child.bananawidget.expand)

    @run_when_ready
    def remove(self, child):
        self._prepare_remove(child)
        child.real_widget.pack_forget()


class Group(Bin, Child):

    def create_widget(self, parent):
        return tk.LabelFrame(parent.real_widget)

    @run_when_ready
    def set_text(self, text):
        self.real_widget['text'] = text
