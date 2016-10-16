"""Canvas widget for BananaGUI."""

import bananagui
from bananagui import _base
from . import bases


@bananagui.bananadoc
class Canvas(_base.Canvas, bases.Child):
    """A canvas widget that you can draw things on.

    When drawing on the canvas, the coordinates can be less than zero or
    greater than the width of the canvas.
    """

    minimum_size = bananagui.Property(
        'minimum_size', how_many=2, type=int, minimum=0, default=(300, 200),
        doc="""Two-tuple of the minimum width and height of the canvas.

        The canvas is smaller than this only if the window is resized
        to something smaller than this.
        """)
    size = bananagui.Property(
        'size', how_many=2, type=int, minimum=0, default=(300, 200),
        settable=False,
        doc="""Two-tuple of the current width and height of the canvas.

        This is updated when the canvas gets resized. The value is
        undefined when the canvas isn't in a visible container.
        """)
    background = bananagui.Property(
        'background', type=bananagui.Color, default=bananagui.WHITE,
        doc="""The background color of the canvas.

        This is the color of the canvas before anything is drawn to it,
        and clearing the canvas fills it with this color.
        """)

    def draw_line(self, start: tuple, end: tuple, *, thickness: int = 1,
                  color: bananagui.Color = bananagui.BLACK) -> None:
        """Draw a line from start to end on the canvas.

        It doesn't matter which position is start and which position is
        end. This method does nothing if color is None.
        """
        assert thickness > 0, "non-positive thickness %r" % (thickness,)
        if color is not None:
            super().draw_line(start, end, thickness, color)

    def draw_polygon(self, *corners, fillcolor: bananagui.Color = None,
                     linecolor: bananagui.Color = bananagui.BLACK,
                     linethickness: int = 1) -> None:
        """Draw a polygon.

        linecolor and fillcolor can be None.
        """
        assert len(corners) > 2, "use draw_line"
        assert linethickness > 0, \
            "non-positive linethickness %r" % (linethickness,)
        if fillcolor is not None or linecolor is not None:
            super().draw_polygon(
                *corners, fillcolor=fillcolor,
                linecolor=linecolor, linethickness=linethickness)

    def draw_oval(self, center: tuple, xradius: int, yradius: int, *,
                  fillcolor: bananagui.Color = None,
                  linecolor: bananagui.Color = bananagui.BLACK,
                  linethickness: int = 1) -> None:
        """Draw an oval on the canvas.

        linecolor and fillcolor can be None.
        """
        assert xradius > 0, "non-positive xradius %r" % (xradius,)
        assert yradius > 0, "non-positive yradius %r" % (yradius,)
        assert linethickness > 0, \
            "non-positive line thickness %r" % (linethickness,)
        super().draw_oval(center, xradius, yradius, fillcolor,
                          linecolor, linethickness)

    def draw_circle(self, center: tuple, radius: int, **kwargs) -> None:
        """Draw a circle on the canvas by calling self.draw_oval()."""
        self.draw_oval(center, radius, radius, **kwargs)

    def fill(self, color: bananagui.Color) -> None:
        """Fill the canvas with a color."""
        width, height = self['size']
        self.draw_polygon((0, 0), (0, height), (width, height), (width, 0),
                          fillcolor=self['background'], linecolor=None)

    def clear(self) -> None:
        """Clear the canvas by filling it with its background."""
        self.fill(self['background'])
