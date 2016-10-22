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

"""BananaGUI spinner test."""

from bananagui import gui


class SpinnerWindow(gui.Window):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        mainbox = gui.Box.vertical(self)
        self['child'] = mainbox

        self.spinner = gui.Spinner(mainbox)
        mainbox['children'].append(self.spinner)

        buttonbox = gui.Box.horizontal(mainbox, expand=(True, False))
        mainbox['children'].append(buttonbox)

        startbutton = gui.Button(buttonbox, text="Start",
                                 on_click=[self.start])
        buttonbox['children'].append(startbutton)

        stopbutton = gui.Button(buttonbox, text="Stop",
                                on_click=[self.stop])
        buttonbox['children'].append(stopbutton)

    def start(self, widget):
        self.spinner['spinning'] = True

    def stop(self, widget):
        self.spinner['spinning'] = False


def main():
    with SpinnerWindow(title="Spinner window") as window:
        window['on_destroy'].append(gui.quit)
        gui.main()


if __name__ == '__main__':
    main()
