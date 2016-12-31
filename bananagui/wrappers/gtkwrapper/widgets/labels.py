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

import bananagui
from .basewidgets import Child


justifys = {bananagui.LEFT: Gtk.Justification.LEFT,
            bananagui.CENTER: Gtk.Justification.CENTER,
            bananagui.RIGHT: Gtk.Justification.RIGHT}
aligns = {bananagui.LEFT: Gtk.Align.START,
          bananagui.CENTER: Gtk.Align.FILL,
          bananagui.RIGHT: Gtk.Align.END}


class Label(Child):

    def __init__(self, bananawidget):
        self.real_widget = Gtk.Label(justify=Gtk.Justification.CENTER)
        super().__init__(bananawidget)

    def set_text(self, text):
        self.real_widget.set_text(text)

    def set_align(self, align):
        self.real_widget.set_halign(aligns[align])
        self.real_widget.set_justify(justifys[align])

    # TODO: implement set_image.