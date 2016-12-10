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

from bananagui import mainloop, widgets


def set_progress(progressbar, spinbox):
    progressbar.progress = spinbox.value / 100


def toggle_bouncing(progressbar, checkbox):
    progressbar.bouncing = checkbox.checked


def main():
    with widgets.Window(title="Progress bar test") as window:
        box = widgets.Box.vertical(window)
        window.child = box

        # A regular progress bar.
        progressbar = widgets.Progressbar(box, expand=(True, False))
        box.append(progressbar)

        spinbox = widgets.Spinbox(box, valuerange=range(101),
                                  expand=(True, False))
        spin_callback = functools.partial(set_progress, progressbar)
        spinbox.on_value_changed.append(spin_callback)
        box.append(spinbox)

        box.append(widgets.Dummy(box))

        # A bouncing progress bar.
        bouncingbar = widgets.BouncingProgressbar(box, expand=(True, False))
        box.append(bouncingbar)

        checkbox = widgets.Checkbox(box, "Bouncing", expand=(True, False))
        check_callback = functools.partial(toggle_bouncing, bouncingbar)
        checkbox.on_checked_changed.append(check_callback)
        box.append(checkbox)

        window.on_close.append(mainloop.quit)
        mainloop.run()


if __name__ == '__main__':
    main()
