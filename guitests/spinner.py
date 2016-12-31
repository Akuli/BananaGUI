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


def start(spinner):
    spinner.spinning = True
    print(spinner)


def stop(spinner):
    spinner.spinning = False
    print(spinner)


def main():
    with widgets.Window("Spinner window") as window:
        mainbox = widgets.Box.vertical()
        window.add(mainbox)

        spinner = widgets.Spinner()
        mainbox.append(spinner)

        buttonbox = widgets.Box.horizontal(expand=(True, False))
        mainbox.append(buttonbox)

        startbutton = widgets.Button("Start")
        startbutton.on_click.connect(start, spinner)
        buttonbox.append(startbutton)

        stopbutton = widgets.Button("Stop")
        stopbutton.on_click.connect(stop, spinner)
        buttonbox.append(stopbutton)

        window.on_close.connect(mainloop.quit)
        mainloop.run()


if __name__ == '__main__':
    main()
