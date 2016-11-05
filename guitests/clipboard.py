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

from bananagui import gui


class ClipboardTestWindow(gui.Window):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        mainbox = gui.Box.vertical(self)
        self['child'] = mainbox

        self.entry = gui.Entry(mainbox, expand=(True, False))
        mainbox['children'].append(self.entry)

        mainbox['children'].append(gui.Dummy(mainbox))

        buttonbox = gui.Box.horizontal(mainbox, expand=(True, False))
        mainbox['children'].append(buttonbox)

        copybutton = gui.Button(buttonbox, text="Copy everything")
        copybutton['on_click'].append(self.copy)
        buttonbox['children'].append(copybutton)

        pastebutton = gui.Button(buttonbox, text="Paste to the end")
        pastebutton['on_click'].append(self.paste)
        buttonbox['children'].append(pastebutton)

    def copy(self, event):
        gui.set_clipboard_text(self.entry['text'])

    def paste(self, event):
        self.entry['text'] += gui.get_clipboard_text()


def main():
    with ClipboardTestWindow(title="Clipboard test") as window:
        window['on_close'].append(gui.quit)
        gui.main()


if __name__ == '__main__':
    main()
