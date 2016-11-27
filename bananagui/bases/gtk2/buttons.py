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


import ctypes

from .libs import _connect, gtk


@debug.debug_class
class BaseButton:

    def __init__(self, parent, **kwargs):
        self.real_widget = gtk.gtk_button_new()
        _connect(self.real_widget, 'clicked', self._do_click)
        super().__init__(parent, **kwargs)

    def _do_click(self):
        self.run_callbacks('on_click')


@debug.debug_class
class Button:

    def _set_text(self, text):
        gtk.gtk_button_set_label(self.real_widget, text.encode('utf-8'))


@debug.debug_class
class ImageButton:

    def __init__(self, parent, **kwargs):
        raise NotImplementedError  # TODO
