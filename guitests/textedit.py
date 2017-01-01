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

"""BananaGUI TextEdit test."""

import bananagui
from bananagui import mainloop, widgets


def text_changed(textedit):
    print("text changed to", repr(textedit.text))


def clear(textview):
    textview.text = ''


def add_text(textedit):
    textedit.text += " Click!"


def main():
    with widgets.Window("TextEdit test", minimum_size=(300, 200)) as window:
        bigbox = widgets.Box()
        window.add(bigbox)

        textedit = widgets.TextEdit("Enter something...")
        textedit.on_text_changed.connect(text_changed, textedit)
        bigbox.append(textedit)

        buttonbox = widgets.Box(bananagui.HORIZONTAL, expand=(True, False))
        bigbox.append(buttonbox)

        addbutton = widgets.Button("Add text")
        addbutton.on_click.connect(add_text, textedit)
        buttonbox.append(addbutton)

        clearbutton = widgets.Button("Clear")
        clearbutton.on_click.connect(clear, textedit)
        buttonbox.append(clearbutton)

        selectallbutton = widgets.Button("Select all")
        selectallbutton.on_click.connect(textedit.select_all)
        buttonbox.append(selectallbutton)

        focusbutton = widgets.Button("Focus")
        focusbutton.on_click.connect(textedit.focus)
        buttonbox.append(focusbutton)

        window.on_close.connect(mainloop.quit)
        mainloop.run()


if __name__ == '__main__':
    main()
