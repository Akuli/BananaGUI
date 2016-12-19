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

from bananagui import mainloop, widgets


class SpinnerWindow(widgets.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        mainbox = widgets.Box.vertical(self)
        self.child = mainbox

        self.spinner = widgets.Spinner(mainbox)
        mainbox.append(self.spinner)

        buttonbox = widgets.Box.horizontal(mainbox, expand=(True, False))
        mainbox.append(buttonbox)

        startbutton = widgets.Button(buttonbox, "Start")
        startbutton.on_click.append(self.start)
        buttonbox.append(startbutton)

        stopbutton = widgets.Button(buttonbox, "Stop")
        stopbutton.on_click.append(self.stop)
        buttonbox.append(stopbutton)

    def start(self, startbutton):
        self.spinner.spinning = True
        print(self.spinner)

    def stop(self, stopbutton):
        self.spinner.spinning = False
        print(self.spinner)


def main():
    with SpinnerWindow("Spinner window") as window:
        window.on_close.append(mainloop.quit)
        mainloop.run()


if __name__ == '__main__':
    main()
