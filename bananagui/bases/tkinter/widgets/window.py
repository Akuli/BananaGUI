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


class _BaseWindow(Bin):

    def __init__(self, bananawidget, title):
        super().__init__(bananawidget)
        self.real_widget.title(title)
        self.real_widget.bind('<Configure>', self._do_configure)
        self.real_widget.protocol('WM_DELETE_WINDOW', self._do_delete)

    def _do_configure(self, event):
        if event.widget is self.real_widget:
            # The event was created by this window, so we can set the
            # current window size based on it. The window is smaller
            # than the minimum size when it's not yet fully showing.
            minwidth, minheight = self.real_widget.minsize()
            if event.width >= minwidth or event.height >= minheight:
                self.bananawidget.size = (event.width, event.height)
        else:
            # A child changed, let's make sure the minimum_size is set
            # correctly.
            self.set_minimum_size(self.bananawidget.minimum_size)

    def _do_delete(self):
        self.bananawidget.run_callbacks('on_close')

    def set_title(self, title):
        self.real_widget.title(title)

    def set_resizable(self, resizable):
        self.real_widget.resizable(resizable, resizable)

    def set_size(self, size):
        self.real_widget.geometry('%dx%d' % size)

    def set_minimum_size(self, size):
        # Tkinter's windows don't avoid becoming too small by default.
        minwidth = max(size[0], self.real_widget.winfo_reqwidth())
        minheight = max(size[1], self.real_widget.winfo_reqheight())
        self.real_widget.minsize(minwidth, minheight)

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


class Window(_BaseWindow):

    def __init__(self, bananawidget, title):
        # This will default to mainloop's root.
        self.real_widget = tk.Toplevel()
        super().__init__(bananawidget, title)


class Dialog(_BaseWindow):

    def __init__(self, bananawidget, parentwindow, title):
        self.real_widget = tk.Toplevel(parentwindow.real_widget)
        super().__init__(bananawidget, title)
