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


class BaseWindow:

    def __init__(self, **kwargs):
        self.real_widget.title(self.title)
        self.real_widget.bind('<Configure>', self._do_configure)
        self.real_widget.protocol(
            'WM_DELETE_WINDOW', self._do_deletewindow)
        self.__setting_size = False
        super().__init__(**kwargs)

    def _do_configure(self, event):
        # I have no idea why the window becomes ridiculously small
        # without this __setting_size guard thingy.
        self.__setting_size = True
        try:
            self.size = (event.width, event.height)
        except AssertionError:
            # The window is currently smaller than the minimum size but
            # it will expand it in a moment.
            pass
        self.__setting_size = False

    def _do_deletewindow(self):
        self.run_callbacks('on_close')

    def _set_title(self, title):
        self.real_widget.title(title)

    def _set_resizable(self, resizable):
        self.real_widget.resizable(resizable, resizable)

    def _set_size(self, size):
        if not self.__setting_size:
            self.real_widget.geometry('%dx%d' % size)

    def _set_minimum_size(self, size):
        width, height = size
        if width is None:
            width = 1
        if height is None:
            height = 1
        self.real_widget.minsize(width, height)

    def _set_showing(self, showing):
        if showing:
            self.real_widget.deiconify()
        else:
            self.real_widget.withdraw()

    def _close(self):
        try:
            self.real_widget.destroy()
        except tk.TclError:
            # The widget has already been closed.
            pass

    def _wait(self):
        self.real_widget.wait_window()

    def _focus(self):
        self.real_widget.lift()
        self.real_widget.attributes('-topmost', True)


class Window:

    def __init__(self, **kwargs):
        # Tkinter will use the root window from the mainloop module.
        self.real_widget = tk.Toplevel()
        super().__init__(**kwargs)


class Dialog:

    def __init__(self, **kwargs):
        self.real_widget = tk.Toplevel(self.parentwindow.real_widget)
        super().__init__(**kwargs)


def colordialog(parentwindow, color, title):
    rgb, hex = colorchooser.askcolor(
        color, title=title,
        parent=parentwindow.real_widget)
    return hex      # This may be None.
