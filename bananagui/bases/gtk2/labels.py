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

from .libs import gtk, GTK_JUSTIFY_CENTER


class BaseLabel:
    pass
    
    
class Label:

    def __init__(self, parent, **kwargs):
        self.real_widget = gtk.gtk_label_new(b"")
        gtk.gtk_label_set_justify(self.real_widget, GTK_JUSTIFY_CENTER)
        super().__init__(parent, **kwargs)

    def _set_text(self, text):
        gtk.gtk_label_set_text(self.real_widget, text.encode('utf-8'))


class ImageLabel:

    def __init__(self, parent, **kwargs):
        raise NotImplementedError  # TODO: use GtkImage here
