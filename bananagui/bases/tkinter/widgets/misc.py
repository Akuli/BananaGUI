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
from .. import mainloop


class Checkbox:

    def __init__(self, parent, **kwargs):
        self._tkinter_var = tk.IntVar()
        self._tkinter_var.trace('w', self._tkinter_var_changed)

        self.real_widget = tk.Checkbutton(
            parent.real_widget, variable=self._tkinter_var)

        # The checkboxes have white foreground on a white background by
        # default with my dark GTK+ theme.
        box_bg = mainloop._convert_color(self.real_widget['selectcolor'])
        checkmark = mainloop._convert_color(self.real_widget['fg'])
        if brightness(box_bg) < 0.5 and brightness(checkmark) < 0.5:
            # Make the background of the actual box where the checkmark
            # goes white, and leave the checkmark dark.
            self.real_widget['selectcolor'] = '#ffffff'
        if brightness(box_bg) >= 0.5 and brightness(checkmark) >= 0.5:
            # Make the background black and leave the checkmark light.
            # This runs with my GTK+ theme.
            self.real_widget['selectcolor'] = '#000000'

        super().__init__(parent, **kwargs)

    def _tkinter_var_changed(self, name, empty_string, mode):
        self.checked = bool(self._tkinter_var.get())

    def _set_text(self, text):
        self.real_widget['text'] = text

    def _set_checked(self, checked):
        self._tkinter_var.set(1 if checked else 0)


class Dummy:

    def __init__(self, parent, **kwargs):
        self.real_widget = tk.Frame(parent.real_widget)
        super().__init__(parent, **kwargs)


class Separator:

    def __init__(self, parent, **kwargs):
        widget = tk.Frame(parent.real_widget, border=1, relief='sunken')
        if self.orientation == bananagui.HORIZONTAL:
            widget['height'] = 3
        if self.orientation == bananagui.VERTICAL:
            widget['width'] = 3
        self.real_widget = widget
        super().__init__(parent, **kwargs)


def set_clipboard_text(text):
    mainloop.root.clipboard_clear()
    mainloop.root.clipboard_append(text)


def get_clipboard_text():
    try:
        return mainloop.root.clipboard_get()
    except tk.TclError:
        # There's nothing on the clipboard.
        return ''
