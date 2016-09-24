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

"""BananaGUI PlainTextView test."""

import sys

from bananagui import gui


class TextViewWindow(gui.Window):

    def __init__(self):
        super().__init__()

        box = gui.VBox(self)
        self['child'] = box

        self.textview = gui.PlainTextView(box)
        self.textview['text'] = "Enter something..."
        self.textview['text.changed'].append(self.text_changed)
        box.add_start(self.textview, expand=True)

        button = gui.Button(box)
        button['text'] = "Click me"
        button['on_click'].append(self.on_click)
        box.add_start(button)

    def text_changed(self, event):
        print(event.new_value)

    def on_click(self, event):
        with self.textview.blocked('text.changed'):
            self.textview.append_text("\nClick!")


def main():
    with TextViewWindow() as window:
        window['title'] = "Textview test"
        window['minimum_size'] = (300, 200)
        window['destroyed.changed'].append(gui.MainLoop.stop)
        sys.exit(gui.MainLoop.run())


if __name__ == '__main__':
    main()
