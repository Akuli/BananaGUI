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

from bananagui import Orient, mainloop, widgets


def value_changed(called_widget, *other_widgets):
    for widget in other_widgets:
        # This doesn't recurse too much because changed callbacks
        # don't run if the old and new value are equal.
        widget.value = called_widget.value


def main():
    values = range(0, 51, 5)

    window = widgets.Window("Slider test", minimum_size=(300, 200))
    mainbox = widgets.Box(Orient.HORIZONTAL)
    window.add(mainbox)

    left_side = widgets.Box()
    hslider = widgets.Slider(values, expand=(True, False))
    spinbox = widgets.Spinbox(values, expand=(True, False))
    left_side.extend([
        widgets.Dummy(), hslider,
        widgets.Dummy(), spinbox,
        widgets.Dummy()])
    mainbox.append(left_side)

    vslider = widgets.Slider(values, Orient.VERTICAL)
    mainbox.append(vslider)

    # Python's sets are awesome.
    all_widgets = {hslider, vslider, spinbox}
    for this in all_widgets:
        others = all_widgets - {this}
        this.on_value_changed.connect(value_changed, this, *others)

    window.on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
