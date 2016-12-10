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

import collections
import math

# We can only import modules from bananagui.widgets because this file
# can be loaded by bananagui.gui.__init__.
import bananagui
from bananagui import color, mainloop
from bananagui.widgets import canvas


_LINES = 15
_DELAY = 60


class Spinner:

    def __init__(self, parent, **kwargs):
        self._widget = canvas.Canvas(parent, minimum_size=(25, 25))
        self.base = self._widget.base
        self._positions = collections.deque()
        for i in range(_LINES):
            #          /|
            #         / |
            #        /  |
            #       /   |
            #      /    |
            #   1 /     | y
            #    /      |
            #   /       |
            #  / angle  |
            # /_)_______|
            #     x
            #
            # sin(angle) = y / 1  =>  y = sin(angle)
            # cos(angle) = x / y  =>  x = cos(angle)
            angle = 360 * i // _LINES
            y = math.sin(math.radians(angle))
            x = math.cos(math.radians(angle))
            self._positions.append((x, y))
        super().__init__(parent, **kwargs)

    def _draw(self):
        self._widget.clear()

        if not self.spinning:
            # We're not spinning anymore.
            return None

        width, height = self._widget.current_size
        diameter = min(width, height)

        # Rotating by a positive number would make the spinner spin
        # counter-clockwise.
        self._positions.rotate(-1)

        for index, (x, y) in enumerate(self._positions):
            brightness = index * 255 // _LINES
            start = (x * diameter // 5 + width // 2,
                     y * diameter // 5 + height // 2)
            end = (x * diameter // 2 + width // 2,
                   y * diameter // 2 + height // 2)
            thickness = max(diameter // 10, 1)
            the_color = color.rgb2hex([brightness] * 3)
            self._widget.draw_line(start, end, thickness=thickness,
                                   color=the_color)

        # Keep spinning.
        return bananagui.RUN_AGAIN

    def _set_spinning(self, spinning):
        if spinning:
            # Start spinning.
            mainloop.add_timeout(_DELAY, self._draw)
        # We don't need an else because _draw knows when to stop.
