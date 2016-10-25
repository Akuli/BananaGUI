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


def set_progress(progressbar, event):
    progressbar['progress'] = event.widget ['value'] / 100


def toggle_bouncing(progressbar, event):
    if event.widget['checked']:
        progressbar['bouncing'] = True
    else:
        progressbar['bouncing'] = False


def main():
    with gui.Window(title="Progress bar test") as window:
        box = gui.Box.vertical(window)
        window['child'] = box

        # A regular progress bar.
        progressbar = gui.Progressbar(box, expand=(True, False))
        box['children'].append(progressbar)

        spin_callback = functools.partial(set_progress, progressbar)
        spinbox = gui.Spinbox(box, valuerange=range(101), expand=(True, False))
        spinbox['value.changed'].append(spin_callback)
        box['children'].append(spinbox)

        box['children'].append(gui.Dummy(box))

        # A bouncing progress bar.
        bouncingbar = gui.BouncingProgressbar(box, expand=(True, False))
        box['children'].append(bouncingbar)

        check_callback = functools.partial(toggle_bouncing, bouncingbar)
        checkbox = gui.Checkbox(box, text="Bouncing", expand=(True, False))
        checkbox['checked.changed'].append(check_callback)
        box['children'].append(checkbox)

        window['on_destroy'].append(gui.quit)
        gui.main()


if __name__ == '__main__':
    main()
