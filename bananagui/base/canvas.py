"""Canvas widget for BananaGUI."""

from bananagui import Color, Property, WHITE
from bananagui.check import check


def _check_fillable_args(fillcolor, linecolor, linethickness):
    assert fillcolor is None or isinstance(fillcolor, bananagui.Color)
    assert linecolor is None or isinstance(linecolor, bananagui.Color)
    assert isinstance(linethickness, int) and linethickness > 0


class Canvas:
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

    _bananagui_bases = ('ChildBase',)
    size = Property('size', pair=True, required_type=int, minimum=1,
                    default=(300, 200))
    background = Property('background', required_type=Color, default=WHITE)

    def draw_line(self, pos1, pos2, *, thickness=1, color=bananagui.BLACK):
        """Draw a line from start to end on the canvas.

        Thickness needs to be a non-negative integer, but it can be 0.
        """
        check(pos1, pair=True, required_type=int)
        check(pos2, pair=True, required_type=int)
        check(thickness, required_type=int, minimum=0)
        check(color, required_type=Color)
        if thickness != 0:
            super().draw_line(pos1, pos2, thickness, color)

    def draw_polygon(self, *positions, fillcolor=None,
                     linecolor=bananagui.BLACK, linethickness=1):
        """Draw a polygon."""
        assert len(positions) > 2, "use draw_line"
        for pos in positions:
            check(pos, pair=True, required_type=int)
        _check_fillable_args(fillcolor, linecolor, linethickness)
        super().draw_polygon(*positions, fillcolor=fillcolor,
                             linecolor=linecolor, linethickness=linethickness)

    def draw_oval(self, centerpos, xradius, yradius, *, fillcolor=None,
                  linecolor=bananagui.BLACK, linethickness=1):
        """Draw an oval on the canvas."""
        check(centerpos, pair=True, required_type=int)
        check(xradius, required_type=int, minimum=1)
        check(yradius, required_type=int, minimum=2)
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
