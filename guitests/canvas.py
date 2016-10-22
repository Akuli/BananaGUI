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

import bananagui
from bananagui import gui


def main():
    with gui.Window(title="Canvas test") as window:
        canvas = gui.Canvas(window, minimum_size=(400, 400))
        window['child'] = canvas

        canvas.draw_line((100, 100), (200, 100))
        canvas.draw_polygon((100, 100), (100, 200), (200, 200),
                            fillcolor=bananagui.RED, linecolor=bananagui.BLUE,
                            linethickness=3)
        canvas.draw_oval((300, 300), 200, 100, fillcolor=bananagui.CYAN,
                         linecolor=bananagui.ORANGE, linethickness=5)
        canvas.draw_circle((300, 300), 50, fillcolor=bananagui.ORANGE,
                           linecolor=bananagui.RED, linethickness=10)

        window['on_destroy'].append(gui.quit)
        gui.main()


if __name__ == '__main__':
    main()
