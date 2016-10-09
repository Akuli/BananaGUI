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

"""BananaGUI checkbox test."""

import sys

from bananagui import gui


class CheckboxWindow(gui.Window):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        checkbox = gui.Checkbox(self, text="Click me!")
        checkbox.checked.changed.connect(self.on_check)
        self['child'] = checkbox

    def on_check(self, event):
        if event.new_value:
            print("You checked me!")
            event.widget['text'] = "Uncheck me!"
        else:
            print("You unchecked me!")
            event.widget['text'] = "Check me!"


def main():
    with CheckboxWindow(title="Checkbox test", size=(200, 50),
                        resizable=False) as window:
        window.destroyed.changed.connect(gui.quit)
        gui.main()


if __name__ == '__main__':
    main()
