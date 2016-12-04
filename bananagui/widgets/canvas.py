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

"""A canvas widget for BananaGUI."""

import bananagui
from bananagui import color
from .basewidgets import Child

_base = bananagui._get_base('widgets.canvas')


# TODO: implement an Image that allows drawing things on it instead of
#       a widget that does tihs

class Canvas(_base.Canvas, Child):
    """A canvas widget that you can draw things on.

    When drawing on the canvas, the coordinates can be less than zero or
    greater than the width of the canvas.

    Attributes:
      minimum_size      Two-tuple of minimum width and height.
                        The canvas is smaller than this only if the
                        window is resized to something smaller than
                        this. This is (300, 200) by default.
      current_size      Two-tuple of the current width and height.
    """

    can_focus = True

    def __init__(self, parent, **kwargs):
        self._minimum_size = self.current_size = (300, 200)
        super().__init__(parent, **kwargs)

    @property
    def minimum_size(self):
        return self._minimum_size

    @minimum_size.setter
    def minimum_size(self, size):
        self._set_minimum_size(size)
        self._minimum_size = size

    def draw_line(self, start, end, *, thickness=1, color=color.BLACK):
        """Draw a line from start to end on the canvas.

        start and end should be two-tuples of coordinates. It doesn't
        matter which position is start and which position is end.
        """
        assert thickness > 0
        super().draw_line(start, end, thickness, color)

    def draw_polygon(self, *corners, fillcolor=None,
                     linecolor=color.BLACK, linethickness=1):
        """Draw a polygon.

        corners should be two-tuples of coordinates. linecolor and
        fillcolor can be None.
        """
        assert len(corners) > 2, "use draw_line"
        assert linethickness > 0
        if fillcolor is not None or linecolor is not None:
            super().draw_polygon(
                *corners, fillcolor=fillcolor,
                linecolor=linecolor, linethickness=linethickness)

    def draw_oval(self, center, xradius, yradius, *, fillcolor=None,
                  linecolor=color.BLACK, linethickness=1):
        """Draw an oval on the canvas.

        linecolor and fillcolor can be None.
        """
        assert xradius > 0
        assert yradius > 0
        assert linethickness > 0
        super().draw_oval(center, xradius, yradius, fillcolor,
                          linecolor, linethickness)

    def draw_circle(self, center, radius, **kwargs) -> None:
        """Draw a circle on the canvas by calling self.draw_oval()."""
        self.draw_oval(center, radius, radius, **kwargs)

    def fill(self, color):
        """Fill the canvas with a color."""
        width, height = self.size
        self.draw_polygon((0, 0), (0, height), (width, height), (width, 0),
                          fillcolor=self.background, linecolor=None)

    def clear(self):
        """Remove everything that has been drawn."""
        super().clear()
