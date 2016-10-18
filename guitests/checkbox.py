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

"""BananaGUI checkbox test."""

from bananagui import gui


def on_check(event):
    if event.new_value:
        print("You checked me!")
        event.widget['text'] = "Uncheck me!"
    else:
        print("You unchecked me!")
        event.widget['text'] = "Check me!"


def main():
    with gui.Window(title="Checkbox test", size=(200, 50)) as window:
        checkbox = gui.Checkbox(window, text="Check me!")
        checkbox['checked.changed'].append(on_check)
        window['child'] = checkbox
        window['on_destroy'].append(gui.quit)
        gui.main()


if __name__ == '__main__':
    main()
