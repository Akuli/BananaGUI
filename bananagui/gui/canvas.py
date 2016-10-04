"""Canvas widget for BananaGUI."""

from bananagui import _base
from bananagui.color import Color, BLACK, WHITE
from bananagui.types import Property, bananadoc
from .bases import ChildBase


@bananadoc
class Canvas(_base.Canvas, ChildBase):
    """A canvas widget that you can draw things on.

    When drawing on the canvas, the coordinates can be less than zero or
    greater than the width of the canvas.
    """

    size = Property(
        'size', pair=True, required_type=int, minimum=1, default=(300, 200),
        doc="""Two-tuple of the width and height of the canvas.

        The actual size may be bigger than this if the canvas is set to
        expand in its parent.
        """)
    background = Property(
        'background', required_type=Color, default=WHITE,
        doc="""The background color of the canvas.

        This is the color of the canvas before anything is drawn to it,
        and clearing the canvas fills it with this color.
        """)

    def draw_line(self, pos1: tuple, pos2: tuple, *, thickness: int = 1,
                  color: Color = BLACK):
        """Draw a line from start to end on the canvas.

        Thickness needs to be a non-negative integer. If it's 0, this
        method does nothing.
        """
        assert thickness >= 0, "negative thickness %r" % (thickness,)
        if thickness != 0:
            super().draw_line(pos1, pos2, thickness, color)

    def draw_polygon(self, *positions, fillcolor: Color = None,
                     linecolor: Color = BLACK, linethickness: int = 1):
        """Draw a polygon.

        Set linethickness to zero if you don't want a border line.
        """
        assert len(positions) > 2, "use draw_line"
        super().draw_polygon(*positions, fillcolor=fillcolor,
                             linecolor=linecolor, linethickness=linethickness)

    def draw_oval(self, centerpos: tuple, xradius: int, yradius: int, *,
                  fillcolor: Color = None, linecolor: Color = BLACK,
                  linethickness: int = 1):
        """Draw an oval on the canvas.

        Set linethickness to zero if you don't want a border line.
        """
        assert xradius > 0, "non-positive xradius %r" % (xradius,)
        assert yradius > 0, "non-positive yradius %r" % (yradius,)
        super().draw_oval(centerpos, xradius, yradius, fillcolor,
                          linecolor, linethickness)

    def draw_circle(self, center: tuple, radius: int, **kwargs):
        """Draw a circle on the canvas by calling self.draw_oval()."""
        self.draw_oval(center, radius, radius, **kwargs)

    def clear(self):
        """Clear the canvas by filling it with its background."""
        width, height = self['size']
        self.draw_polygon((0, 0), (0, height), (width, height), (width, 0),
                          fillcolor=self['background'], linethickness=0)
