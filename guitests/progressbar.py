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

from bananagui import mainloop, widgets


def set_progress(progressbar, spinbox):
    progressbar.progress = spinbox.value / 100
    print(progressbar)


def set_bouncing(bouncingbar, checkbox):
    bouncingbar.bouncing = checkbox.checked
    print(bouncingbar)


def main():
    window = widgets.Window("Progress bar test")
    box = widgets.Box()
    window.add(box)

    progressbar = widgets.Progressbar(expand=(True, False))
    box.append(progressbar)

    spinbox = widgets.Spinbox(valuerange=range(101), expand=(True, False))
    spinbox.on_value_changed.connect(set_progress, progressbar, spinbox)
    box.append(spinbox)

    box.append(widgets.Dummy())

    bouncingbar = widgets.BouncingProgressbar(expand=(True, False))
    box.append(bouncingbar)

    checkbox = widgets.Checkbox("Bouncing", expand=(True, False))
    checkbox.on_checked_changed.connect(
        set_bouncing, bouncingbar, checkbox)
    box.append(checkbox)

    window.on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
