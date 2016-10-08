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


def on_check(event, entry):
    entry['read_only'] = event.widget['checked']


def on_click(event, entry):
    print(entry['text'])


def select_all(event, entry):
    entry.select_all()


def main():
    with gui.Window() as window:
        vbox = gui.VBox(window)
        window['child'] = vbox

        entry = gui.Entry(vbox)
        vbox.append(entry)

        hbox = gui.HBox(vbox)
        vbox.append(hbox)

        printbutton = gui.Button(hbox)
        printbutton['text'] = "Print it"
        printbutton.on_click.connect(on_click, entry)
        hbox.append(printbutton)

        selectallbutton = gui.Button(hbox)
        selectallbutton['text'] = "Select all"
        selectallbutton.on_click.connect(select_all, entry)
        hbox.append(selectallbutton)

        checkbox = gui.Checkbox(hbox)
        checkbox['text'] = "Read only"
        checkbox.checked.changed.connect(on_check, entry)
        hbox.append(checkbox)

        window['title'] = "Entry test"
        window['size'] = (200, 50)
        window['resizable'] = False
        window.destroyed.changed.connect(gui.quit)
        gui.main()


if __name__ == '__main__':
    main()
