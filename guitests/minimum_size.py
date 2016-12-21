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

"""BananaGUI size test."""

from bananagui import mainloop, widgets

instructions = ("The window should always fully show\n"
                "this text and the button you clicked.")


def click_callback(button):
    box = button.parent
    label = box[0]
    if button.text == "Hide instructions":
        label.text = 'hidden'
        button.text = "Show instructions"
    else:
        label.text = instructions
        button.text = "Hide instructions"


def main():
    # minimum_size=(1, 1) tests if setting it on initialization makes
    # a difference (it shouldn't).
    with widgets.Window("Minimum size test",
                        minimum_size=(1, 1)) as window:
        box = widgets.Box.vertical(window)
        window.child = box
        box.append(widgets.Label(box, 'hidden'))
        button = widgets.Button(box, "Show instructions")
        button.on_click.append(click_callback)
        box.append(button)
        window.on_close.append(mainloop.quit)
        mainloop.run()


if __name__ == '__main__':
    main()