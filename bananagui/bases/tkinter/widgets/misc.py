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
from bananagui.color import brightness

from .basewidgets import Child
from .. import mainloop


class Checkbox(Child, tk.Checkbutton):

    def __init__(self, widget, parent):
        self._var = tk.IntVar()
        self._var.trace('w', self._var_changed)
        super().__init__(widget, parent, parent.base, variable=self._var)

        # The checkboxes have white foreground on a white background by
        # default with my dark GTK+ theme.
        box_bg = mainloop._convert_color(self['selectcolor'])
        checkmark = mainloop._convert_color(self['fg'])
        if brightness(box_bg) < 0.5 and brightness(checkmark) < 0.5:
            # Make the background of the actual box where the checkmark
            # goes white, and leave the checkmark dark.
            self['selectcolor'] = '#ffffff'
        if brightness(box_bg) >= 0.5 and brightness(checkmark) >= 0.5:
            # Make the background black and leave the checkmark light.
            # This runs with my GTK+ theme.
            self['selectcolor'] = '#000000'

        self.bananawidget = widget

    def _var_changed(self, name, empty_string, mode):
        self.bananawidget.checked = (self._var.get() != 0)

    def set_text(self, text):
        self['text'] = text

    def set_checked(self, checked):
        self._var.set(1 if checked else 0)


class Dummy(Child, tk.Frame):

    def __init__(self, widget, parent):
        super().__init__(widget, parent, parent.base)


class Separator(Child, tk.Frame):

    def __init__(self, widget, parent, orientation):
        super().__init__(widget, parent, parent.base)
        self['border'] = 1
        self['relief'] = 'sunken'
        if orientation == bananagui.HORIZONTAL:
            self['height'] = 3
        if orientation == bananagui.VERTICAL:
            self['width'] = 3


def set_clipboard_text(text):
    mainloop.root.clipboard_clear()
    mainloop.root.clipboard_append(text)


def get_clipboard_text():
    try:
        return mainloop.root.clipboard_get()
    except tk.TclError:
        # There's nothing on the clipboard.
        return ''
