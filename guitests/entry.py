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

"""BananaGUI entry test."""

import sys

from bananagui import gui


class EntryWindow(gui.Window):

    def __init__(self):
        super().__init__()

        box = gui.HBox(self)
        self['child'] = box

        # This entry is attached to self because the on_click method
        # needs it.
        self.entry = gui.Entry(box)
        self.entry['text'] = "Enter something here..."
#        self.entry['hidden'] = True
        box.add_start(self.entry, expand=True)

        checkbox = gui.Checkbox(box)
        checkbox['text'] = "Read only"
        checkbox['checked.changed'].append(self.on_check)
        box.add_start(checkbox)

        button = gui.Button(box)
        button['text'] = "Print it"
        button['on_click'].append(self.on_click)
        box.add_start(button)

    def on_click(self, event):
        print(self.entry['text'])

    def on_check(self, event):
        self.entry['read_only'] = event.widget['checked']


def main():
    with EntryWindow() as window:
        window['title'] = "Entry test"
        window['size'] = (200, 100)
        window['minimum_size'] = (100, 50)
        window['destroyed.changed'].append(gui.MainLoop.quit)
        sys.exit(gui.MainLoop.run())


if __name__ == '__main__':
    main()
