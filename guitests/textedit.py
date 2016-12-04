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

"""BananaGUI TextEdit test."""

from bananagui import mainloop, widgets


class TextEditWindow(widgets.Window):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        bigbox = widgets.Box.vertical(self)
        self.child = bigbox

        self.textedit = widgets.TextEdit(bigbox, text="Enter something...")
        self.textedit.on_text_changed.append(self.text_changed)
        bigbox.append(self.textedit)

        buttonbox = widgets.Box.horizontal(bigbox, expand=(True, False))
        bigbox.append(buttonbox)

        addbutton = widgets.Button(buttonbox, text="Add text")
        addbutton.on_click.append(self.add_text)
        buttonbox.append(addbutton)

        clearbutton = widgets.Button(buttonbox, text="Clear")
        clearbutton.on_click.append(self.clear)
        buttonbox.append(clearbutton)

        selectallbutton = widgets.Button(buttonbox, text="Select all")
        selectallbutton.on_click.append(self.select_all)
        buttonbox.append(selectallbutton)

    def text_changed(self, textedit):
        print("text changed to %r" % textedit.text)

    def add_text(self, addbutton):
        self.textedit.text += " Click!"

    def select_all(self, selectallbutton):
        self.textedit.select_all()
        self.textedit.focus()

    def clear(self, clearbutton):
        self.textedit.text = ''


def main():
    with TextEditWindow(title="TextEdit test",
                        minimum_size=(300, 200)) as window:
        window.on_close.append(mainloop.quit)
        mainloop.run()


if __name__ == '__main__':
    main()
