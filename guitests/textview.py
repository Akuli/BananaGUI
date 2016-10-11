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


class TextviewWindow(gui.Window):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        bigbox = gui.Box.vertical(self)
        self['child'] = bigbox

        self.textview = gui.PlainTextView(bigbox, text="Enter something...")
        self.textview['text.changed'].append(self.text_changed)
        bigbox.append(self.textview)

        buttonbox = gui.Box.horizontal(bigbox, expand=(True, False))
        bigbox.append(buttonbox)

        insertbutton = gui.Button(buttonbox, text="Append text",
                                  on_click=[self.append_text])
        buttonbox.append(insertbutton)

        clearbutton = gui.Button(buttonbox, text="Clear",
                                 on_click=[self.clear])
        buttonbox.append(clearbutton)

        selectallbutton = gui.Button(buttonbox, text="Select all",
                                     on_click=[self.select_all])
        buttonbox.append(selectallbutton)

    def text_changed(self, event):
        print(event.new_value)

    def append_text(self, event):
        self.textview.append_text(" Click!")

    def select_all(self, event):
        self.textview.select_all()

    def clear(self, event):
        self.textview.clear()


def main():
    with TextviewWindow(title="Textview test",
                        minimum_size=(300, 200)) as window:
        window['destroyed.changed'].append(gui.quit)
        gui.main()


if __name__ == '__main__':
    main()
