"""Canvas widget for BananaGUI."""

from bananagui import _base
from bananagui.check import check
from bananagui.color import Color, BLACK, WHITE
from bananagui.types import Property, bananadoc
from .bases import ChildBase


def _check_fillable_args(fillcolor, linecolor, linethickness):
    check(fillcolor, required_type=Color, allow_none=True)
    check(linecolor, required_type=Color, allow_none=True)
    check(linethickness, required_type=int, minimum=0)


@bananadoc
class Canvas(_base.Canvas, ChildBase):
    """A canvas widget that you can draw things on.

    When drawing on the canvas, the coordinates can be less than zero or
    greater than the width of the canvas.

    Properties:
        size            RW
            Two-tuple of width and height.
            (300, 200) by default. The actual size may be bigger
            depending on what kind of layout widget the canvas is in.
        background      RW
            Background of the canvas.
            This must be a BananaGUI color, and this is WHITE by
            default.
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
        check(pos1, pair=True, required_type=int)
        check(pos2, pair=True, required_type=int)
        assert isinstance(thickness, int) and thickness >= 0
        assert isinstance(color, Color)
        if thickness != 0:
            super().draw_line(pos1, pos2, thickness, color)

    def draw_polygon(self, *positions, fillcolor=None,
                     linecolor=BLACK, linethickness=1):
        """Draw a polygon."""
        assert len(positions) > 2, "use draw_line"
        for pos in positions:
            check(pos, pair=True, required_type=int)
        _check_fillable_args(fillcolor, linecolor, linethickness)
        super().draw_polygon(*positions, fillcolor=fillcolor,
                             linecolor=linecolor, linethickness=linethickness)

    def draw_oval(self, centerpos, xradius, yradius, *, fillcolor=None,
                  linecolor=BLACK, linethickness=1):
        """Draw an oval on the canvas."""
        check(centerpos, pair=True, required_type=int)
        assert isinstance(xradius, int) and xradius > 0
        assert isinstance(yradius, int) and yradius > 0
        _check_fillable_args(fillcolor, linecolor, linethickness)
        super().draw_oval(centerpos, xradius, yradius, fillcolor,
                          linecolor, linethickness)

    def draw_circle(self, center, radius, **kwargs):
        """Draw a circle on the canvas."""
        self.draw_oval(center, radius, radius, **kwargs)

    def clear(self):
        """Clear the canvas by filling it with its background."""
        width, height = self['size']
        self.draw_polygon((0, 0), (0, height), (width, height), (width, 0),
                          fillcolor=self['background'], linethickness=0)
