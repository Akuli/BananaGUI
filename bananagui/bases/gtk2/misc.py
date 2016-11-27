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

from .libs import _connect, gdk, gtk


@debug.debug_class
class Checkbox:

    def __init__(self, parent, **kwargs):
        self.real_widget = gtk.gtk_check_button_new()
        _connect(self.real_widget, 'notify::active', self._do_check)
        super().__init__(parent, **kwargs)

    def _do_check(self):
        self.checked = bool(gtk.gtk_toggle_button_get_active(self.real_widget))

    def _set_text(self, text):
        gtk.gtk_button_set_label(self.real_widget, text.encode('utf-8'))

    def _set_checked(self, checked):
        gtk.gtk_toggle_button_set_active(checked)


@debug.debug_class
class Dummy:

    def __init__(self, parent, **kwargs):
        self.real_widget = gtk.gtk_label_new(b"")
        super().__init__(parent, **kwargs)


@debug.debug_class
class Separator:
    ...


set_clipboard_text = get_clipboard_text = get_font_families = ...
