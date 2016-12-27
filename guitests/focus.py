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

"""Focusing GUI test."""

import functools

from bananagui import mainloop, widgets


def on_click(other_button, this_button):
    other_button.focus()


def main():
    message = ("Press tab and then enter. The focus\n"
               "should move to the other button.")

    with widgets.Window("Focus test", minimum_size=(250, 150)) as window:
        box = widgets.Box.vertical()
        window.child = box

        label = widgets.Label(message)
        box.append(label)

        button1 = widgets.Button("Focus the button below")
        button2 = widgets.Button("Focus the button above")
        button1.on_click.append(functools.partial(on_click, button2))
        button2.on_click.append(functools.partial(on_click, button1))
        box.extend([button1, button2])

        window.on_close.append(mainloop.quit)
        mainloop.run()


if __name__ == '__main__':
    main()
