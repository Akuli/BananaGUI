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

from .basewidgets import Child, run_when_ready


def _setup_bindings(bananawidget, tkinterwidget):
    def callback(event):
        bananawidget.select_all()
        return 'break'

    tkinterwidget.bind('<Control-A>', callback)
    tkinterwidget.bind('<Control-a>', callback)


class Entry(Child):

    def create_widget(self, parent):
        self._var = tk.StringVar()
        self._var.trace('w', self._var_changed)
        widget = tk.Entry(parent.real_widget, textvariable=self._var)
        _setup_bindings(self.bananawidget, widget)
        return widget

    def _var_changed(self, tkname, empty_string, mode):
        self.bananawidget.text = self._var.get()

    @run_when_ready
    def set_text(self, text):
        self._var.set(text)

    # This overrides the set_grayed_out defined in basewidgets.py.
    @run_when_ready
    def set_grayed_out(self, grayed_out):
        self.real_widget['state'] = 'readonly' if grayed_out else 'normal'

    @run_when_ready
    def set_secret(self, secret):
        self.real_widget['show'] = '*' if secret else ''

    @run_when_ready
    def select_all(self):
        self.real_widget.selection_range(0, 'end')


class TextEdit(Child):

    def create_widget(self, parent):
        # A larger width or height would prevent the widget from
        # shrinking when needed.
        widget = tk.Text(parent.real_widget, width=1, height=1)
        widget.bind('<<Modified>>', self._on_modified)
        _setup_bindings(self.bananawidget, widget)
        return widget

    # TODO: the cursor likes to jump to the end of the widget and
    # "modified" prints too often...

    def _on_modified(self, event):
        print('modified')
        self.bananawidget.text = event.widget.get(0.0, 'end-1c')
        event.widget.edit_modified(False)

    @run_when_ready
    def set_text(self, text):
        print('setting text')
        self.real_widget.unbind('<<Modified>>')
        self.real_widget.delete(0.0, 'end-1c')
        self.real_widget.edit_modified(False)
        self.real_widget.bind('<<Modified>>', self._on_modified)
        self.real_widget.insert(0.0, text)

    @run_when_ready
    def set_grayed_out(self, grayed_out):
        self.real_widget['state'] = 'disable' if grayed_out else 'normal'

    @run_when_ready
    def select_all(self):
        # The end-1c doesn't get what tkinter thinks of as the last
        # character, which is a hidden newline.
        self.real_widget.tag_add('sel', 0.0, 'end-1c')
