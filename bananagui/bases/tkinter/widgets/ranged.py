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


class Slider:

    def __init__(self, parent, **kwargs):
        minimum = min(self.valuerange)
        maximum = max(self.valuerange)
        step = utils.rangestep(self.valuerange)
        widget = tk.Scale(parent.real_widget, from_=minimum,
                          to=maximum, resolution=step,
                          orient=tkinter_orients[self.orientation])

        # There seems to be no way to change a Scale's value with the
        # keyboard so this seems to work. There's a stackoverflow answer
        # that recommends binding <Button1-Release>, but it doesn't
        # change the value immediately when the scale is moved.
        widget.bind('<Button1-Motion>', self._on_motion)
        self.real_widget = widget
        super().__init__(parent, **kwargs)

    def _on_motion(self, event):
        # This doesn't do anything if the value hasn't changed.
        self.value = event.widget.get()

    def _set_value(self, value):
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


class Spinbox:

    def __init__(self, parent, **kwargs):
        self._tkinter_var = tk.StringVar()
        self._tkinter_var.trace('w', self._tkinter_var_changed)

        widget = tk.Spinbox(
            parent.real_widget, textvariable=self._tkinter_var,
            # Tkinter doesn't know how to handle ranges.
            values=tuple(self.valuerange))
        widget.bind('<Control-A>', _select_all)
        widget.bind('<Control-a>', _select_all)
        self.real_widget = widget
        super().__init__(parent, **kwargs)

    def _tkinter_var_changed(self, tkname, empty_string, mode):
        try:
            value = int(self._tkinter_var.get())
            if value not in self.valuerange:
                return
        except ValueError:
            return
        self.value = value

    def _set_value(self, value):
        # This tells tkinter to call self._tkinter_var_changed and the
        # callbacks are ran.
        self._tkinter_var.set(str(value))
