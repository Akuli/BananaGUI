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
from bananagui import color

from .basewidgets import Child, run_when_ready
from .. import mainloop


class Checkbox(Child):

    def __init__(self, bananawidget):
        self._var = tk.IntVar()
        self._var.trace('w', self._var_changed)
        super().__init__(bananawidget)

    def create_widget(self, parent):
        widget = tk.Checkbutton(parent.real_widget, variable=self._var)

        # The checkboxes have white foreground on a white background by
        # default with my dark GTK+ theme.
        box_bg = mainloop._convert_color(widget['selectcolor'])
        checkmark = mainloop._convert_color(widget['fg'])
        if box_bg == checkmark:
            if color.brightness(box_bg) > 0.8:
                # It's really light, make it black.
                widget['fg'] = color.BLACK
            elif color.brightness(box_bg) < 0.2:
                # It's really dark, make it white.
                widget['fg'] = color.WHITE
            else:
                # Fall back to the background and hope it's different
                # enough...
                widget['fg'] = widget['bg']
#        if brightness(box_bg) < 0.5 and brightness(checkmark) < 0.5:
#            # Make the background of the actual box where the checkmark
#            # goes white, and leave the checkmark dark.
#            widget['selectcolor'] = '#ffffff'
#        if brightness(box_bg) >= 0.5 and brightness(checkmark) >= 0.5:
#            # Make the background black and leave the checkmark light.
#            # This runs with my GTK+ theme.
#            widget['selectcolor'] = '#000000'
        return widget

    def _var_changed(self, name, empty_string, mode):
        self.bananawidget.checked = (self._var.get() != 0)

    @run_when_ready
    def set_text(self, text):
        self.real_widget['text'] = text

    # The variable was created in __init__, so we don't need
    # @run_when_ready.
    def set_checked(self, checked):
        self._var.set(1 if checked else 0)


class Dummy(Child):

    def create_widget(self, parent):
        return tk.Label(parent.real_widget)


class Separator(Child):

    def __init__(self, bananawidget, orientation):
        self.orientation = orientation
        super().__init__(bananawidget)

    def create_widget(self, parent):
        widget = tk.Frame(parent.real_widget, border=1, relief='sunken')
        if self.orientation == bananagui.HORIZONTAL:
            widget['height'] = 3
        if self.orientation == bananagui.VERTICAL:
            widget['width'] = 3
        return widget
