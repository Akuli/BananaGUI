"""Canvas widget for BananaGUI."""

import bananagui
from bananagui import check


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
        assert thickness >= 0, "negative thickness"
        assert isinstance(color, bananagui.Color), \
            "a BananaGUI color is required"
        if thickness != 0:
            super().draw_line(pos1, pos2, thickness, color)

    def draw_polygon(self, *positions, fillcolor=None, linethickness=1,
                     linecolor=bananagui.BLACK):
        """Draw a polygon."""
        assert len(positions) > 2, "use draw_line"
        for pos in positions:
            check.intpair(pos)
        for color in (fillcolor, linecolor):
            assert isinstance(fillcolor, bananagui.Color)
        assert isinstance(linethickness, int)
        assert linethickness >= 0
        assert isinstance(color, bananagui.Color)
        super().draw_polygon(*positions, fillcolor=fillcolor,
                             linethickness=linethickness, linecolor=linecolor)

    def draw_oval(self, centerpos, xradius, yradius, *, fillcolor=None,
                  linecolor=bananagui.BLACK, linethickness=1):
        """Draw an oval on the canvas."""
        check.intpair(centerpos)
        for radius in (xradius, yradius):
            assert isinstance(radius, int), "radiuses must be integers"
            assert radius > 0, "too small radius"
        assert fillcolor is None or isinstance(fillcolor, bananagui.Color), \
            "None or a BananaGUI color is required"
        assert isinstance(linecolor, bananagui.Color), \
            "a BananaGUI color is required"
        assert isinstance(linethickness, int), \
            "line thickness must be an integer"
        assert linethickness >= 0, "negative line thickness"
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
