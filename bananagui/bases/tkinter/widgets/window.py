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

from .containers import Bin


class Window(Bin):

    def __init__(self, bananawidget, parentwindow=None):
        if parentwindow is None:
            # BananaGUI Window, this will default to mainloop's root.
            self.real_widget = tk.Toplevel()
        else:
            # BananaGUI Dialog.
            self.real_widget = tk.Toplevel(parentwindow.real_widget)
        super().__init__(bananawidget)
        self.real_widget.title('')  # Get rid of the default title.
        self.real_widget.bind('<Configure>', self._do_configure)
        self.real_widget.protocol('WM_DELETE_WINDOW', self._do_delete)
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
        self.real_widget.title(title)

    def set_resizable(self, resizable):
        self.real_widget.resizable(resizable, resizable)

    def set_size(self, size):
        if not self._setting_size:
            self.real_widget.geometry('%dx%d' % size)

    def set_minimum_size(self, size):
        width, height = size
        if width is None:
            width = 1
        if height is None:
            height = 1
        self.real_widget.minsize(width, height)

    def set_hidden(self, hidden):
        if hidden:
            self.real_widget.withdraw()
        else:
            self.real_widget.deiconify()

    def close(self):
        try:
            self.real_widget.destroy()
        except tk.TclError:
            # The widget has already been closed.
            pass

    def wait(self):
        # TODO: a modal wait_for method for Window objects.
        self.real_widget.wait_window()

    def focus(self):
        self.real_widget.lift()
        self.real_widget.attributes('-topmost', True)


Dialog = Window
