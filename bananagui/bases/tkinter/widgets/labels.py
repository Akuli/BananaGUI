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

from .basewidgets import Child


class Label(Child):

    def __init__(self, bananawidget, parent):
        self.real_widget = tk.Label(parent.real_widget)
        super().__init__(bananawidget, parent)

    def set_text(self, text):
        self.real_widget['text'] = text

    def set_path(self, path):
        if path is None:
            # Remove the old image if any.
            self._image = self.real_widget['image'] = ''
        else:
            # Tkinter needs a reference to the PhotoImage to avoid
            # garbage collection.
            self._image = self.real_widget['image'] = tk.PhotoImage(file=path)


ImageLabel = Label
