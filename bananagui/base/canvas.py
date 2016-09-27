"""Canvas widget for BananaGUI."""

import bananagui
from bananagui import utils, check
#from bananagui import structures, types, utils


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
    size = bananagui.Property('size', checker=check.positive_intpair,
                              default=(300, 200))
    background = bananagui.Property(
        'background', required_type=bananagui.Color,
        default=bananagui.WHITE)

    def draw_line(self, pos1, pos2, *, thickness=1, color=bananagui.BLACK):
        """Draw a line from start to end on the canvas.

        Thickness needs to be a non-negative integer, but it can be 0.
        """
        for pos in (pos1, pos2):
            check.intpair(pos)
        assert isinstance(thickness, int), "the thickness must be an integer"
        assert thickness >= 0, "negative thicknesses aren't allowed"
        assert isinstance(color, bananagui.Color), \
            "%r is not a BananaGUI color" % color
        if thickness != 0:
            super().draw_line(pos1, pos2, thickness, color)

    def draw_polygon(self, *positions, fillcolor=None, linethickness=1,
                     linecolor=structures.BLACK):
        """Draw a polygon."""
        if len(positions) < 3:
            raise ValueError("at least 3 positions are needed for "
                             "drawing a polygon")
        for pos in positions:
            utils.check_integer_pair(pos)
        for color in (fillcolor, linecolor):
            assert isinstance(fillcolor, bananagui.Color), \
                "fillcolor must be a BananaGUI Color"
        self.draw_line(*positions[:2], 0, linecolor)  # Check the arguments.
        utils.check(linethickness, required_type=int, minimum=0)
        super().draw_polygon(*positions, fillcolor=fillcolor,
                             linethickness=linethickness, linecolor=linecolor)

    def draw_oval(self, centerpos, xradius, yradius, *, fillcolor=None,
                  linecolor=structures.BLACK, linethickness=1):
        """Draw an oval on the canvas."""
        utils.check_integer_pair(centerpos)
        utils.check(xradius, required_type=int, minimum=1)
        utils.check(yradius, required_type=int, minimum=1)
        utils.check(fillcolor, required_type=structures.Color, allow_none=True)
        utils.check(linecolor, required_type=structures.Color)
        utils.check(linethickness, required_type=int, minimum=0)
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
