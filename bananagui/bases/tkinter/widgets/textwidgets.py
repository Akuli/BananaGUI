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


class TextBase:

    def __init__(self, parent, **kwargs):
        self.real_widget.bind('<Control-A>', self._on_control_a)
        self.real_widget.bind('<Control-a>', self._on_control_a)
        super().__init__(parent, **kwargs)

    def _on_control_a(self, event):
        self.select_all()
        return 'break'


class Entry:

    def __init__(self, parent, **kwargs):
        self._tkinter_var = tk.StringVar()
        self._tkinter_var.trace('w', self._tkinter_var_changed)
        widget = tk.Entry(parent.real_widget, textvariable=self._tkinter_var)
        self.real_widget = widget
        super().__init__(parent, **kwargs)

    def _tkinter_var_changed(self, tkname, empty_string, mode):
        self.text = self._tkinter_var.get()

    def _set_text(self, text):
        self._tkinter_var.set(text)

    # This overrides the _set_grayed_out defined in basewidgets.py.
    def _set_grayed_out(self, grayed_out):
        state = 'readonly' if grayed_out else 'normal'
        self.real_widget['state'] = state

    def _set_secret(self, secret):
        self.real_widget['show'] = '*' if secret else ''

    def _select_all(self):
        self.real_widget.selection_range(0, 'end')


class TextEdit:

    def __init__(self, parent, **kwargs):
        # TODO: Add more keyboard shortcuts.
        # A larger width or height would prevent the widget from
        # shrinking when needed.
        self.real_widget = tk.Text(parent.real_widget, width=1, height=1)
        self.real_widget.bind('<<Modified>>', self._on_modified)
        super().__init__(parent, **kwargs)

    def _select_all(self):
        """Select all text in the widget."""
        # The end-1c doesn't get what tkinter thinks of as the last
        # character, which is a hidden newline.
        self.real_widget.tag_add('sel', 0.0, 'end-1c')

    # TODO: the cursor likes to jump to the end of the widget and
    # "modified" prints too often...

    def _on_modified(self, event):
        print('modified')
        self.text = event.widget.get(0.0, 'end-1c')
        self.real_widget.edit_modified(False)

    def _set_text(self, text):
        print('setting text')
        self.real_widget.unbind('<<Modified>>')
        self.real_widget.delete(0.0, 'end-1c')
        self.real_widget.edit_modified(False)
        self.real_widget.bind('<<Modified>>', self._on_modified)
        self.real_widget.insert(0.0, text)

    def _set_grayed_out(self, grayed_out):
        self.real_widget['state'] = 'disable' if grayed_out else 'normal'
