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


from .libs import GCallback, gobject, gtk


class Widget:

    def __init__(self):
        # Things that tend to be garbage collected too early can be
        # added here.
        self._dont_garbage_collect = []

    def _focus(self):
        gtk.gtk_widget_grab_focus(self.real_widget)


class Parent:
    pass


class Child:

    def _set_expand(self, expand):
        pass    # TODO

    def _set_tooltip(self, tooltip):
        gtk.gtk_widget_set_tooltip_text(
            self.real_widget, tooltip.encode('utf-8'))

    def _set_grayed_out(self, grayed_out):
        gtk.gtk_widget_set_sensitive(self.real_widget, not grayed_out)
