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

from . import orientations
from .basewidgets import Child


class Checkbox(Child):

    def __init__(self, bananawidget):
        self.real_widget = Gtk.CheckButton()
        self.real_widget.connect('notify::active', self._do_check)
        super().__init__(bananawidget)

    def _do_check(self, real_widget, gparam):
        self.bananawidget.checked = real_widget.get_active()

    def set_text(self, text):
        self.real_widget.set_label(text)

    def set_checked(self, checked):
        self.real_widget.set_active(checked)


class Dummy(Child):

    def __init__(self, bananawidget):
        self.real_widget = Gtk.Label()
        super().__init__(bananawidget)


class Separator(Child):

    def __init__(self, bananawidget, orientation):
        gtk_orientation = orientations[orientation]
        self.real_widget = Gtk.Separator(orientation=gtk_orientation)
        super().__init__(bananawidget)
