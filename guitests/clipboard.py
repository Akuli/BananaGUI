# Copyright (c) 2016-2017 Akuli

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

import bananagui
from bananagui import clipboard, mainloop, widgets


def copy_from_entry(entry):
    clipboard.set_text(entry.text)


def paste_to_entry(entry):
    text = clipboard.get_text()
    if text is None:
        print("there's no text on the clipboard")
    else:
        entry.text += text


def main():
    window = widgets.Window("Clipboard test")
    mainbox = widgets.Box()
    window.add(mainbox)

    entry = widgets.Entry(expand=(True, False))
    mainbox.append(entry)

    mainbox.append(widgets.Dummy())

    buttonbox = widgets.Box(bananagui.HORIZONTAL, expand=(True, False))
    mainbox.append(buttonbox)

    copybutton = widgets.Button("Copy everything")
    copybutton.on_click.connect(copy_from_entry, entry)
    buttonbox.append(copybutton)

    pastebutton = widgets.Button("Paste to the end")
    pastebutton.on_click.connect(paste_to_entry, entry)
    buttonbox.append(pastebutton)

    window.on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
