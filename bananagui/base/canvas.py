"""Canvas widget for BananaGUI."""

from bananagui import Property, check


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
    size = Property('size', checker=check.positive_intpair, default=(300, 200))
    background = Property('background', required_type=bananagui.Color,
                          default=bananagui.WHITE)

    def draw_line(self, pos1, pos2, *, thickness=1, color=bananagui.BLACK):
        """Draw a line from start to end on the canvas.

        Thickness needs to be a non-negative integer, but it can be 0.
        """
        for pos in (pos1, pos2):
            check.intpair(pos)
        assert isinstance(thickness, int)
        assert thickness >= 0
        assert isinstance(color, bananagui.Color)
        if thickness != 0:
            super().draw_line(pos1, pos2, thickness, color)

    def __check_fillable_kwargs(self, fillcolor, linecolor, linethickness):
        assert fillcolor is None or isinstance(fillcolor, bananagui.Color)
        assert linecolor is None or isinstance(linecolor, bananagui.Color)
        assert isinstance(linethickness, int)
        assert linethickness >= 0

    def draw_polygon(self, *positions, fillcolor=None,
                     linecolor=bananagui.BLACK, linethickness=1):
        """Draw a polygon."""
        assert len(positions) > 2, "use draw_line"
        for pos in positions:
            check.pair(pos, required_type=int)
        self.__check_fillable_kwargs(fillcolor, linecolor, linethickness)
        super().draw_polygon(*positions, fillcolor=fillcolor,
                             linecolor=linecolor, linethickness=linethickness)

    def draw_oval(self, centerpos, xradius, yradius, *, fillcolor=None,
                  linecolor=bananagui.BLACK, linethickness=1):
        """Draw an oval on the canvas."""
        check.pair(centerpos, required_type=int)
        for radius in (xradius, yradius):
            assert isinstance(radius, int)
            assert radius > 0
        self.__check_fillable_kwargs(fillcolor, linecolor, linethickness)
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
