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

from bananagui import utils
from . import tkinter_orients
from .basewidgets import Child


class Slider(Child):

    def __init__(self, bananawidget, parent, orientation, valuerange):
        minimum = min(valuerange)
        maximum = max(valuerange)
        step = utils.rangestep(valuerange)
        self.real_widget = tk.Scale(
            parent.real_widget, from_=minimum, to=maximum,
            resolution=step, orient=tkinter_orients[orientation])
        # There seems to be no way to change a Scale's value with the
        # keyboard so this seems to work. There's a stackoverflow answer
        # that recommends binding <ButtonRelease-1>, but it doesn't
        # change the value immediately when the scale is moved.
        self.real_widget.bind('<Button1-Motion>', self._on_motion)

        super().__init__(bananawidget, parent)

    def _on_motion(self, event):
        # This doesn't do anything if the value hasn't changed.
        self.bananawidget.value = event.widget.get()

    def set_value(self, value):
        self.real_widget.set(value)


def _select_all(event):
    try:
        # Tkinter's spinboxes don't have a selection_range method for
        # some reason, but entries have it.
        event.widget.selection('range', 0, 'end')
    except tk.TclError:
        # Maybe selection_range doesn't work with spinboxes on old Tk
        # versions?
        pass


class Spinbox(Child):

    def __init__(self, bananawidget, parent, valuerange):
        self._var = tk.StringVar()
        self._var.trace('w', self._var_changed)

        self.real_widget = tk.Spinbox(
            parent.real_widget,
            # Tkinter doesn't know how to handle ranges.
            values=tuple(valuerange))
        print('real_widget' in dir(self))
        self.real_widget.bind('<Control-A>', _select_all)
        self.real_widget.bind('<Control-a>', _select_all)

        # The textvariable needs to be set after setting bananawidget
        # with super().__init__().
        super().__init__(bananawidget, parent)
        self.real_widget['textvariable'] = self._var

    def _var_changed(self, tkname, empty_string, mode):
        try:
            value = int(self._var.get())
            if value not in self.bananawidget.valuerange:
                return
        except ValueError:
            return
        self.bananawidget.value = value

    def set_value(self, value):
        # This tells tkinter to call self._tkinter_var_changed and the
        # callbacks are ran.
        self._var.set(str(value))
