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
from tkinter import colorchooser

from .containers import Bin


class Window(Bin, tk.Toplevel):

    def __init__(self, widget, parentwindow=None):
        if parentwindow is None:
            # BananaGUI Window.
            super().__init__(widget)
        else:
            # BananaGUI Dialog.
            super().__init__(widget, parentwindow.base)
        self.bananawidget = widget
        self.title('')
        self.bind('<Configure>', self._do_configure)
        self.protocol('WM_DELETE_WINDOW', self._do_delete)
        self._setting_size = False

    def _do_configure(self, event):
        # The window is smaller than the minimum size when it's not
        # fully showing yed.
        min_width, min_height = self.bananawidget.minimum_size
        if min_width is not None and event.width < min_width:
            return
        if min_height is not None and event.height < min_height:
            return

        # I have no idea why the window becomes ridiculously small
        # without this _setting_size guard thingy.
        self._setting_size = True
        self.bananawidget.size = (event.width, event.height)
        self._setting_size = False

    def _do_delete(self):
        self.bananawidget.run_callbacks('on_close')

    def set_title(self, title):
        self.title(title)

    def set_resizable(self, resizable):
        self.resizable(resizable, resizable)

    def set_size(self, size):
        if not self._setting_size:
            self.geometry('%dx%d' % size)

    def set_minimum_size(self, size):
        width, height = size
        if width is None:
            width = 1
        if height is None:
            height = 1
        self.minsize(width, height)

    def set_hidden(self, hidden):
        if hidden:
            self.withdraw()
        else:
            self.deiconify()

    def close(self):
        try:
            self.destroy()
        except tk.TclError:
            # The widget has already been closed.
            pass

    def wait(self):
        self.wait_window()

    def focus(self):
        self.lift()
        self.attributes('-topmost', True)


Dialog = Window
