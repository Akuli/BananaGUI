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

import functools

import bananagui
from bananagui import gui


class SliderBox(gui.Box):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, orientation=bananagui.VERTICAL, **kwargs)

        values = range(0, 51, 5)

        hslider = gui.Slider.horizontal(self, valuerange=values)
        hslider.on_value_changed.append(self.value_changed)
        self.append(hslider)

        vslider = gui.Slider.vertical(self, valuerange=values)
        vslider.on_value_changed.append(self.value_changed)
        self.append(vslider)

        spinbox = gui.Spinbox(self, valuerange=values)
        spinbox.on_value_changed.append(self.value_changed)
        self.append(spinbox)

    def value_changed(self, called_widget):
        widgets = list(self)
        widgets.remove(called_widget)
        for widget in widgets:
            # This doesn't recurse too much because callbacks don't run
            # if the old and new value are equal.
            widget.value = called_widget.value


def main():
    with gui.Window(title="Slider test") as window:
        window.child = SliderBox(window)
        window.on_close.append(gui.quit)
        gui.main()


if __name__ == '__main__':
    main()
