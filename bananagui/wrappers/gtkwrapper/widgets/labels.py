# Copyright (c) 2016-2017 Akuli

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

from bananagui import Align
from .basewidgets import Child


haligns_and_justifys = {
    Align.LEFT: (Gtk.Align.START, Gtk.Justification.LEFT),
    Align.CENTER: (Gtk.Align.CENTER, Gtk.Justification.FILL),
    Align.RIGHT: (Gtk.Align.END, Gtk.Justification.RIGHT),
}


class Label(Child):

    def __init__(self, bananawidget):
        self.widget = Gtk.Label(justify=Gtk.Justification.CENTER)
        super().__init__(bananawidget)

    def set_text(self, text):
        self.widget.set_text(text)

    def set_align(self, align):
        halign, justify = haligns_and_justifys[align]
        self.widget.set_halign(halign)
        self.widget.set_justify(justify)

    # TODO: implement set_image.
