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

import bananagui
from bananagui import mainloop, widgets


def set_grayed_out(entry, checkbox):
    entry.grayed_out = checkbox.checked


def set_secret(entry, checkbox):
    entry.secret = checkbox.checked

    
def reset_text(entry):
    entry.text = "Enter something..."


def main():
    with widgets.Window("Entry test") as window:
        entrybox = widgets.Box.vertical()
        window.add(entrybox)

        entry = widgets.Entry("Enter something...", expand=(True, False))
        entry.on_text_changed.connect(print, entry)
        entrybox.append(entry)

        entrybox.append(widgets.Dummy())

        buttonbox = widgets.Box.horizontal(expand=(True, False))
        entrybox.append(buttonbox)

        resetbutton = widgets.Button("Reset")
        resetbutton.on_click.connect(reset_text, entry)
        buttonbox.append(resetbutton)

        selectallbutton = widgets.Button("Select all")
        selectallbutton.on_click.connect(entry.select_all)
        buttonbox.append(selectallbutton)

        focusbutton = widgets.Button("Focus")
        focusbutton.on_click.connect(entry.focus)
        buttonbox.append(focusbutton)

        grayed = widgets.Checkbox("Grayed out")
        grayed.on_checked_changed.connect(set_grayed_out, entry, grayed)
        buttonbox.append(grayed)

        secret = widgets.Checkbox("Secret")
        secret.on_checked_changed.connect(set_secret, entry, secret)
        buttonbox.append(secret)

        window.on_close.connect(mainloop.quit)
        mainloop.run()


if __name__ == '__main__':
    main()
