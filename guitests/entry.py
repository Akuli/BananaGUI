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


class EntryBox(widgets.Box):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, orientation=bananagui.VERTICAL, **kwargs)

        # This is attached to self because we need it in other methods.
        self.entry = widgets.Entry(self, expand=(True, False))
        self.entry.on_text_changed.append(self.text_changed)
        self.append(self.entry)

        self.append(widgets.Dummy(self))

        buttonbox = widgets.Box.horizontal(self, expand=(True, False))
        self.append(buttonbox)

        resetbutton = widgets.Button(buttonbox, "Reset")
        resetbutton.on_click.append(self.reset)
        buttonbox.append(resetbutton)

        selectallbutton = widgets.Button(buttonbox, "Select all")
        selectallbutton.on_click.append(self.select_all)
        buttonbox.append(selectallbutton)

        focusbutton = widgets.Button(buttonbox, "Focus")
        focusbutton.on_click.append(self.get_focus)
        buttonbox.append(focusbutton)

        grayedcheckbox = widgets.Checkbox(buttonbox, "Grayed out")
        grayedcheckbox.on_checked_changed.append(
            self.grayed_out_toggled)
        buttonbox.append(grayedcheckbox)

        secretcheckbox = widgets.Checkbox(buttonbox, "Secret")
        secretcheckbox.on_checked_changed.append(self.secret_toggled)
        buttonbox.append(secretcheckbox)

        self.reset()

    def reset(self, resetbutton=None):
        self.entry.text = "Enter something..."

    def text_changed(self, entry):
        print("text changed to %r" % entry.text)

    def select_all(self, selectallbutton):
        self.entry.select_all()

    # This is get_focus instead of focus. If this was focus, it would
    # be difficult to give focus to this widget when needed, except
    # that it wouldn't really matter because BananaGUI boxes aren't
    # focusable anyway.
    def get_focus(self, focusbutton):
        self.entry.focus()

    def grayed_out_toggled(self, checkbox):
        self.entry.grayed_out = checkbox.checked

    def secret_toggled(self, checkbox):
        self.entry.secret = checkbox.checked


def main():
    with widgets.Window("Entry test", size=(400, 100)) as window:
        window.child = EntryBox(window)
        window.on_close.append(mainloop.quit)
        mainloop.run()


if __name__ == '__main__':
    main()
