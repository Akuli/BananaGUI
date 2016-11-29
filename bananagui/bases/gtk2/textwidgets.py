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

from .libs import _connect, gtk


class TextBase:
    pass


class Entry:

    def __init__(self, parent, **kwargs):
        self.real_widget = gtk.gtk_entry_new()
        _connect(self.real_widget, 'changed', self._do_changed)
        super().__init__(parent, **kwargs)
    
    def _do_changed(self):
        self.text = gtk.gtk_entry_get_text(self.real_widget).decode('utf-8')
        
    def _set_text(self, text):
        gtk.gtk_entry_set_text(self.real_widget, text.encode('utf-8'))
    
    def _set_grayed_out(self, grayed_out):
        gtk.gtk_entry_set_editable(self.real_widget, not grayed_out)
    
    def _set_secret(self, secret):
        gtk.gtk_entry_set_visibility(self.real_widget, not secret)

    def select_all(self):
        gtk.gtk_entry_select_region(self.real_widget, 0, -1)


class TextEdit:
    # TODO: tabchar

    def __init__(self, parent, **kwargs):
        self.real_widget = gtk.gtk_text_view_new()
        self._textbuf = gtk.gtk_text_view_get_buffer(self.real_widget)
        self._changed_id = _connect(self._textbuf, "changed", self._do_changed)
        self.__setting_text = False
        super().__init__(parent, **kwargs)

    def __iters(self):
        return (gtk.gtk_text_buffer_get_start_iter(self._textbuf),
                gtk.gtk_text_buffer_get_end_iter(self._textbuf))

    def _do_changed(self):
        print(1)
        self.__setting_text = True
        print(2)
        args = self.__iters() + (True,)
        print(3)
        text = gtk.gtk_text_buffer_get_text(self._textbuf, *args)
        print(4)
        self.text = text.decode('utf-8')
        print(5)
        self.__setting_text = False
        print(6)

    def select_all(self):
        gtk.gtk_text_buffer_select_range(self._textbuf, *self.__iters())

    def _set_text(self, text):
        # We get weird warnings if we remove this check.
        if not self.__setting_text:
            # gtk_text_buffer_set_text() first clears the buffer and
            # then inserts to it, but we must not run the callback twice.
            gtk.g_signal_handler_block(self._textbuf, self._changed_id)
            gtk.gtk_text_buffer_set_text(self._textbuf, text.encode('utf-8'))
            gtk.g_signal_handler_unblock(self._textbuf, self._changed_id)
