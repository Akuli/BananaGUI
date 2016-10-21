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


class Bin:

    def _bananagui_set_child(self, child):
        if self['child'] is not None:
            self['child']['real_widget'].pack_forget()
            self['child']._bananagui_tkinter_packed = False
        if child is not None:
            child['real_widget'].pack()
            child._bananagui_tkinter_packed = True
            child._bananagui_set_expand(child['expand'])  # See bases.py.


_appendsides = {
    # Appending to a box adds a child to the beginning of the box, and
    # then the next child towards the center from the first child and
    # so on.
    bananagui.HORIZONTAL: 'left',
    bananagui.VERTICAL: 'top',
}


class Box:

    def __init__(self, parent, **kwargs):
        self.real_widget.raw_set(tk.Frame(parent['real_widget']))
        super().__init__(parent, **kwargs)

    def _bananagui_box_append(self, child):
        child['real_widget'].pack(
            side=_appendsides[self['orientation']],
            fill=tkinter_fills[child['expand']],
        )
        child._bananagui_tkinter_packed = True

        # Set the pack expanding, see ChildBase._bananagui_set_expand
        # in bases.py.
        child._bananagui_set_expand(child['expand'])

    def _bananagui_box_remove(self, child):
        child['real_widget'].pack_forget()
        child._bananagui_tkinter_packed = False
