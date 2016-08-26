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

"""BananaGUI TextView test."""

import sys

from bananagui import gui


class TextViewTest(gui.Window):

    def __init__(self):
        super().__init__()

        box = gui.VBox(self)
        self['child'] = box

        # This textview is attached to self because the on_click method
        # needs it.
        self.textview = gui.TextView(box)
        self.textview['text'] = "Enter something here..."
        box.add_start(self.textview, expand=True)

        button = gui.Button(box)
        button['text'] = "Print it"
        button['on_click'].append(self.on_click)
        box.add_start(button)

    def on_click(self, button):
        print(self.textview['text'])


def main():
    gui.init()
    with TextViewTest() as window:
        window['title'] = "TextView test"
        window['minimum_size'] = (300, 200)
        window['destroyed.changed'].append(gui.quit)
        sys.exit(gui.main())


if __name__ == '__main__':
    main()
