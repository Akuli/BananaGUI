"""Canvas widget for BananaGUI."""

from bananagui import _base, Color, BLACK, WHITE, Property, bananadoc
from .bases import Child


@bananadoc
class Canvas(_base.Canvas, Child):
    """A canvas widget that you can draw things on.

    When drawing on the canvas, the coordinates can be less than zero or
    greater than the width of the canvas.
    """

    minimum_size = Property(
        'size', pair=True, type=int, minimum=0, default=(300, 200),
        doc="""Two-tuple of the minimum width and height of the canvas.

        The canvas is smaller than this only if the window is resized
        to something smaller than this.
        """)
    size = Property(
        'size', pair=True, type=int, minimum=0, default=(300, 200),
        settable=False,
        doc="""Two-tuple of the current width and height of the canvas.

        This is updated when the canvas gets resized. The value is
        undefined when the canvas isn't in a visible container.
        """)
    background = Property(
        'background', type=Color, default=WHITE,
        doc="""The background color of the canvas.

        This is the color of the canvas before anything is drawn to it,
        and clearing the canvas fills it with this color.
        """)

    def draw_line(self, pos1: tuple, pos2: tuple, *, thickness: int = 1,
                  color: Color = BLACK):
        """Draw a line from start to end on the canvas.

        This method does nothing if color is None.
        """
        assert thickness > 0, "non-positive thickness %r" % (thickness,)
        if color is not None:
            super().draw_line(pos1, pos2, thickness, color)

    def draw_polygon(self, *positions, fillcolor: Color = None,
                     linecolor: Color = BLACK, linethickness: int = 1):
        """Draw a polygon.

        linecolor and fillcolor can be None.
        """
        assert len(positions) > 2, "use draw_line"
        assert linethickness > 0, \
            "non-positive linethickness %r" % (linethickness,)
        super().draw_polygon(*positions, fillcolor=fillcolor,
                             linecolor=linecolor, linethickness=linethickness)

    def draw_oval(self, centerpos: tuple, xradius: int, yradius: int, *,
                  fillcolor: Color = None, linecolor: Color = BLACK,
                  linethickness: int = 1):
        """Draw an oval on the canvas.

        linecolor and fillcolor can be None.
        """
        assert xradius > 0, "non-positive xradius %r" % (xradius,)
        assert yradius > 0, "non-positive yradius %r" % (yradius,)
        assert linethickness > 0, \
            "non-positive line thickness %r" % (linethickness,)
        super().draw_oval(centerpos, xradius, yradius, fillcolor,
                          linecolor, linethickness)

    def draw_circle(self, center: tuple, radius: int, **kwargs):
        """Draw a circle on the canvas by calling self.draw_oval()."""
        self.draw_oval(center, radius, radius, **kwargs)

    def clear(self):
        """Clear the canvas by filling it with its background."""
        width, height = self['size']
        self.draw_polygon((0, 0), (0, height), (width, height), (width, 0),
                          fillcolor=self['background'], linecolor=None)
