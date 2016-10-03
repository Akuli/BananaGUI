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

    def __init__(self, parent):
        super().__init__(parent)
        self['real_widget'].bind('<Control-A>', self.__select_all)
        self['real_widget'].bind('<Control-a>', self.__select_all)

    def __select_all(self, event):
        self.select_all()
        return 'break'


class Entry:

    def __init__(self, parent):
        self.__var = tk.StringVar()
        self.__var.trace('w', self.__var_changed)

        widget = tk.Entry(parent['real_widget'], textvariable=self.__var)
        self.real_widget.raw_set(widget)

        super().__init__(parent)

    def __var_changed(self, tkname, empty_string, mode):
        self.text.raw_set(self.__var.get())

    def _bananagui_set_text(self, text):
        self.__var.set(text)

    def _bananagui_set_read_only(self, read_only):
        state = 'readonly' if read_only else 'normal'
        self['real_widget'].config(state=state)

    def select_all(self):
        self['real_widget'].selection_range(0, 'end')


class PlainTextView:

    def __init__(self, parent):
        # A larger width or height would prevent the widget from
        # shrinking when needed.
        # TODO: Add more keyboard shortcuts.
        widget = tk.Text(parent['real_widget'], width=1, height=1)
        widget.bind('<<Modified>>', self.__edit_modified)
        self.raw_set('real_widget', widget)
        super().__init__(parent)

    def select_all(self):
        """Select all text in the widget."""
        # The end-1c doesn't get what tkinter thinks of as the last
        # character, which is a newline.
        self['real_widget'].tag_add('sel', 0.0, 'end-1c')

    def __edit_modified(self, event):
        """Update the widget's text property."""
        self.raw_set('text', event.widget.get(0.0, 'end-1c'))

        # This function will be called twice if the event is not unbound
        # first.
        event.widget.unbind('<<Modified>>')

        # Tell tkinter that the text in the widget has not been
        # modified. This will run again when the text is modified.
        event.widget.edit_modified(False)

        # Bind again.
        event.widget.bind('<<Modified>>', self.__edit_modified)

    def clear(self):
        self['real_widget'].delete(0.0, 'end')

    def append_text(self, text):
        self['real_widget'].insert('end', text)
