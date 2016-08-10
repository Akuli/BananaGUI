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

gui = bananagui.get('tkinter')


def on_click():
    """The user clicked the button."""
    print("Clicked!")


window = gui.Window()

box = gui.Box.vbox(window)
window.set_child(box)

label = gui.Label(box)
label.set_text("Click this button:")
box.append(label, expand=True)

button = gui.TextButton(box)
button.set_text("Click me!")
button.set_tooltip("Yes, click me.")
button.on_click.connect(on_click)
box.append(button)

window.set_size([150, 100])
window.on_close.connect(gui.quit)
sys.exit(gui.main())
