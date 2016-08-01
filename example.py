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

import gui


gui = gui.get('tkinter')


def click_callback(pressed):
    """The user pressed or released the button."""
    if pressed:
        print("Pressed!")
    else:
        print("Released!")


window = gui.Window()

mainbox = gui.Box.vbox(window)
window.child(mainbox)

topbox = gui.Box.vbox(mainbox)
mainbox.prepend(topbox)

label = gui.Label(topbox)
label.text("Enter something:")
topbox.append(label, expand=True)

button = gui.TextButton(topbox)
button.text("Click me!")
button.pressed.callbacks.append(click_callback)
topbox.append(button)

window.size((200, 200))
window.showing.callbacks.append(gui.quit)
gui.main()
