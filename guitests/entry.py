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

from bananagui import gui


class EntryWindow(gui.Window):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        bigbox = gui.Box.vertical(self)
        self['child'] = bigbox

        # This is attached to self because we need it in other methods.
        self.entry = gui.Entry(bigbox, text="Enter something...",
                               expand=(True, False))
        bigbox.append(self.entry)

        dummy = gui.Dummy(bigbox)
        bigbox.append(dummy)

        buttonbox = gui.Box.horizontal(bigbox, expand=(True, False))
        bigbox.append(buttonbox)

        printbutton = gui.Button(buttonbox, text="Print it!",
                                 on_click=[self.print_it])
        buttonbox.append(printbutton)

        selectallbutton = gui.Button(buttonbox, text="Select all",
                                     on_click=[self.select_all])
        buttonbox.append(selectallbutton)

        checkbox = gui.Checkbox(buttonbox, text="Read only")
        checkbox['checked.changed'].append(self.read_only_toggled)
        buttonbox.append(checkbox)

    def print_it(self, event):
        print(self.entry['text'])

    def select_all(self, event):
        self.entry.select_all()

    def read_only_toggled(self, event):
        self.entry['read_only'] = event.new_value


def main():
    with EntryWindow(title="Entry test", size=(250, 100)) as window:
        window['destroyed.changed'].append(gui.quit)
        gui.main()


if __name__ == '__main__':
    main()
