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

"""The checkbox wrapper."""

import tkinter as tk

import bananagui.color


class Checkbox:

    def __init__(self, parent):
        super().__init__(parent)

        self.__var = tk.IntVar()
        self.__var.trace('w', self.__var_changed)

        widget = tk.Checkbutton(parent['real_widget'], variable=self.__var)
        self.raw_set('real_widget', widget)

        # The checkboxes have white foreground on a white background by
        # default with my dark GTK+ theme.
        widget_bg = bananagui.color.Color.from_hex(widget.cget('bg'))
        box_bg = bananagui.color.Color.from_hex(widget.cget('selectcolor'))
        checkmark = bananagui.color.Color.from_hex(widget.cget('fg'))
        if box_bg.brightness < 0.5 and checkmark.brightness < 0.5:
            # Make the background of the actual box where the checkmark
            # goes white, and leave the checkmark dark.
            widget.config(selectcolor='#ffffff')
        if box_bg.brightness >= 0.5 and checkmark.brightness >= 0.5:
            # Make the background black and leave the checkmark light.
            # This runs with my GTK+ theme.
            widget.config(selectcolor='#000000')

    def __var_changed(self, name, empty_string, mode):
        self.raw_set('checked', bool(self.__var.get()))

    def _bananagui_set_text(self, text):
        self['real_widget'].config(text=text)

    def _bananagui_set_checked(self, checked):
        self.__var.set(checked)
