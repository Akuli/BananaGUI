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

import bananagui

gui = bananagui.get('bananagui.wrappers.tkinter')


def on_click():
    print("Click!")


window = gui.Window()

box = gui.Box.vbox(window)
window['child'] = box

label = gui.Label(box)
label['text'] = "Click this button:"
box.append(label, expand=True)

button = gui.TextButton(box)
button['text'] = "Click me!"
button['tooltip'] = "Yes, click me."
button['on_click'].append(on_click)
box.append(button)

window['size'] = (150, 100)     # the parentheses can be omitted
window['on_close'].append(gui.quit)
sys.exit(gui.main())
