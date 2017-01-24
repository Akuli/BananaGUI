# Copyright (c) 2016-2017 Akuli

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

from .parents import Bin


class _BaseWindow(Bin):

    def __init__(self, bananawidget, title):
        super().__init__(bananawidget)
        self.widget.title(title)
        self.widget.bind('<Configure>', self._do_configure)
        self.widget.protocol('WM_DELETE_WINDOW', self._do_delete)
        self.widget['border'] = 5  # Looks nicer.
        # The window may jump around randomly sometimes without this.
        self._can_set_size = True

    def add(self, child):
        # This constructs all widgets of the child.
        child.create(self)
        self._real_add(child)   # See basewidgets.py.

    def _do_configure(self, event):
        if event.widget is self.widget:
            # The event was created by this window, so we can set the
            # current window size based on it. The window is smaller
            # than the minimum size when it's not yet fully showing.
            minwidth, minheight = self.widget.minsize()
            if event.width > minwidth and event.height > minheight:
                self._can_set_size = False
                self.bananawidget.size = (event.width, event.height)
                self._can_set_size = True
        else:
            # A child changed, let's make sure the minimum_size is set
            # correctly.
            self.set_minimum_size(self.bananawidget.minimum_size)

    def _do_delete(self):
        self.bananawidget.on_close.run()

    def set_title(self, title):
        self.widget.title(title)

    def set_resizable(self, resizable):
        self.widget.resizable(resizable, resizable)

    def set_size(self, size):
        if self._can_set_size:
            self.widget.geometry('%dx%d' % size)

    def set_minimum_size(self, size):
        # Tkinter's windows don't avoid becoming too small by default.
        minwidth = max(size[0], self.widget.winfo_reqwidth())
        minheight = max(size[1], self.widget.winfo_reqheight())
        self.widget.minsize(minwidth, minheight)

    def set_hidden(self, hidden):
        if hidden:
            self.widget.withdraw()
        else:
            self.widget.deiconify()

    def close(self):
        try:
            self.widget.destroy()
        except tk.TclError:
            # The widget has already been closed.
            pass

    def wait(self):
        # TODO: a modal wait_for method for Window objects.
        self.widget.wait_window()

    def focus(self):
        self.widget.lift()
        self.widget.attributes('-topmost', True)


class Window(_BaseWindow):

    def __init__(self, bananawidget, title):
        # This will default to mainloop's root.
        self.widget = tk.Toplevel()
        super().__init__(bananawidget, title)


class Dialog(_BaseWindow):

    def __init__(self, bananawidget, parentwindow, title):
        self.widget = tk.Toplevel(parentwindow.widget)
        super().__init__(bananawidget, title)
