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

from bananagui import clipboard, mainloop, widgets


class ClipboardTestWindow(widgets.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        mainbox = widgets.Box.vertical(self)
        self.child = mainbox

        self.entry = widgets.Entry(mainbox, expand=(True, False))
        mainbox.append(self.entry)

        mainbox.append(widgets.Dummy(mainbox))

        buttonbox = widgets.Box.horizontal(mainbox, expand=(True, False))
        mainbox.append(buttonbox)

        copybutton = widgets.Button(buttonbox, "Copy everything")
        copybutton.on_click.append(self.copy)
        buttonbox.append(copybutton)

        pastebutton = widgets.Button(buttonbox, text="Paste to the end")
        pastebutton.on_click.append(self.paste)
        buttonbox.append(pastebutton)

    def copy(self, copybutton):
        clipboard.set_text(self.entry.text)

    def paste(self, pastebutton):
        text = clipboard.get_text()
        if text is None:
            print("there's no text on the clipboard")
        else:
            self.entry.text += text


def main():
    with ClipboardTestWindow("Clipboard test") as window:
        window.on_close.append(mainloop.quit)
        mainloop.run()


if __name__ == '__main__':
    main()
