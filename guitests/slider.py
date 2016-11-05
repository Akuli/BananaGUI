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

from bananagui import gui


class SliderWindow(gui.Window):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        box = gui.Box.vertical(self)
        self['child'] = box

        values = range(0, 51, 5)

        self.hslider = gui.Slider.horizontal(box, valuerange=values)
        self.hslider['value.changed'].append(self.value_changed)
        box['children'].append(self.hslider)

        self.vslider = gui.Slider.vertical(box, valuerange=values)
        self.vslider['value.changed'].append(self.value_changed)
        box['children'].append(self.vslider)

        self.spinbox = gui.Spinbox(box, valuerange=values)
        self.spinbox['value.changed'].append(self.value_changed)
        box['children'].append(self.spinbox)

    def value_changed(self, event):
        # Python's sets are awesome.
        all_widgets = {self.hslider, self.vslider, self.spinbox}
        other_widgets = all_widgets - {event.widget}
        for widget in other_widgets:
            widget['value'] = event.new_value


def main():
    with SliderWindow(title="Hello World!") as window:
        window['on_close'].append(gui.quit)
        gui.main()


if __name__ == '__main__':
    main()
