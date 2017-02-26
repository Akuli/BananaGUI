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

from . import orientations
from .basewidgets import Child


class Slider(Child):

    def __init__(self, bananawidget, orientation, valuerange):
        range_args = (min(valuerange), max(valuerange), valuerange.step)
        self.widget = Gtk.Scale.new_with_range(
            orientations[orientation], *range_args)
        self.widget.connect('value-changed', self._do_value_changed)
        super().__init__(bananawidget)

    def _do_value_changed(self, widget):
        value = int(widget.get_value())
        if value in self.bananawidget.valuerange:
            self.bananawidget.value = value
            return

        # TODO: is there a better way to allow only values in the
        # range?
        difference = value - self.bananawidget.value
        step = self.bananawidget.valuerange.step
        if abs(difference) < step/2:
            # Keeping the value where it is now is probably closest
            # to what the user wants.
            widget.set_value(self.bananawidget.value)
        else:
            # Time to move the widget.
            if difference > 0:
                # Let's move the scale up.
                self.bananawidget.value += step
            else:
                # Let's move it down.
                self.bananawidget.value -= step

    def set_value(self, value):
        self.widget.set_value(value)


class Spinbox(Child):

    def __init__(self, bananawidget, valuerange):
        range_args = (min(valuerange), max(valuerange), valuerange.step)
        self.widget = Gtk.SpinButton.new_with_range(*range_args)
        self.widget.connect('notify::value', self._do_value_changed)
        super().__init__(bananawidget)

    def _do_value_changed(self, widget, gparam):
        self.bananawidget.value = widget.get_value_as_int()

    def set_value(self, value):
        self.widget.set_value(value)
