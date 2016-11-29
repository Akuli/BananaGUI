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
        self.real_widget = Gtk.Entry()
        self.real_widget.connect('changed', self._do_changed)
        super().__init__(parent, **kwargs)

    def _do_changed(self, entry):
        self.text = entry.get_text()

    def _set_text(self, text):
        self.real_widget.set_text(text)

    def _set_grayed_out(self, grayed_out):
        self.real_widget.set_editable(not grayed_out)

    def _set_secret(self, secret):
        self.real_widget.set_visibility(not secret)

    def select_all(self):
        self.real_widget.select_region(0, -1)


class TextEdit:
    # TODO: tabchar

    def __init__(self, parent, **kwargs):
        self.real_widget = Gtk.TextView()
        self._textbuf = self.real_widget.get_buffer()
        self._changed_id = self._textbuf.connect('changed', self._do_changed)
        self.__setting_text = False
        super().__init__(parent, **kwargs)

    def _do_changed(self, buf):
        self.__setting_text = True
        self.text = buf.get_text(buf.get_start_iter(),
                                 buf.get_end_iter(), True)
        self.__setting_text = False

    def select_all(self):
        self._textbuf.select_range(self._textbuf.get_start_iter(),
                                   self._textbuf.get_end_iter())

    def _set_text(self, text):
        # We get weird warnings if we remove this check.
        if not self.__setting_text:
            # set_text() first clears the buffer and then inserts to
            # it, but we must not run the callback twice.
            with self._textbuf.handler_block(self._changed_id):
                self._textbuf.set_text(text)
