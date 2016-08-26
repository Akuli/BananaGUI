#!/usr/bin/env python3

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

"""Hello world program."""

import sys

import bananagui
from bananagui import gui

bananagui.load_guiwrapper('.tkinter')


def on_click(button):
    print("You clicked me!")


def main():
    gui.init()

    with gui.Window() as window:
        box = gui.VBox(window)
        window['child'] = box

        label = gui.Label(box)
        label['text'] = "Hello World!"
        box.add_start(label, expand=True)

        button = gui.Button(box)
        button['text'] = "Click me!"
        button['tooltip'] = "Yes, click me."
        button['on_click'].append(on_click)
        box.add_end(button)

        window['title'] = "Hello"
        window['size'] = (150, 100)    # the parentheses can be omitted
        window['minimum_size'] = (100, 70)
        window['destroyed.changed'].append(gui.quit)
        sys.exit(gui.main())


if __name__ == '__main__':
    main()
