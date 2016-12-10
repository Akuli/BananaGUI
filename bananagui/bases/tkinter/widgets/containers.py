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

import tkinter as tk

import bananagui
from . import tkinter_fills
from .basewidgets import Child, Widget


class Bin(Widget):

    def set_child(self, child):
        old_child = self.bananawidget.child
        if old_child is not None:
            old_child.base.pack_forget()
            old_child.base._packed = False
        if child is not None:
            child.base.pack()
            child.base._packed = True
            child.base.set_expand(child.expand)  # Update the packing.


# TODO: Scroller.


_appendsides = {
    # Appending to a box adds a child to the beginning of the box, and
    # then the next child towards the center from the first child and
    # so on.
    bananagui.HORIZONTAL: 'left',
    bananagui.VERTICAL: 'top',
}


class Box(Child, tk.Frame):

    def __init__(self, widget, parent, orientation):
        super().__init__(widget, parent, parent.base)

    def append(self, child):
        child.base.pack(
            side=_appendsides[self.bananawidget.orientation],
            fill=tkinter_fills[child.expand],
        )
        child.base._packed = True
        child.base.set_expand(child.expand)  # Update the packing.

    def remove(self, child):
        child.base.pack_forget()
        child.base._packed = False
