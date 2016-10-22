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

from gi.repository import Gtk


class TextBase:
    pass


class Entry:

    def __init__(self, parent, **kwargs):
        widget = Gtk.Entry()
        widget.connect('changed', self.__changed)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def __changed(self, entry):
        self.text.raw_set(entry.get_text())

    def _bananagui_set_text(self, text):
        self['real_widget'].set_text(text)

    def _bananagui_set_read_only(self, read_only):
        self['real_widget'].set_editable(not read_only)

    def select_all(self):
        self['real_widget'].select_region(0, -1)
        self['real_widget'].grab_focus()


class PlainTextView:
    # TODO: tabchar

    def __init__(self, parent, **kwargs):
        widget = Gtk.TextView()
        self.__buf = widget.get_buffer()
        self.__buf.connect('changed', self.__changed)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def __changed(self, buf):
        self.text.raw_set(buf.get_text(buf.get_start_iter(),
                                       buf.get_end_iter(), True))

    def __bounds(self):
        return self.__buf.get_start_iter(), self.__buf.get_end_iter()

    def select_all(self):
        self.__buf.select_range(self.__buf.get_start_iter(),
                                self.__buf.get_end_iter())
        self['real_widget'].grab_focus()

    def clear(self):
        self.__buf.delete(self.__buf.get_start_iter(),
                          self.__buf.get_end_iter())

    def append_text(self, text):
        self.__buf.insert(self.__buf.get_end_iter(), text)
