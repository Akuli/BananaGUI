import itertools
import tkinter as tk


class Canvas:

    def __init__(self, parent, **kwargs):
        width, height = self['size']
        widget = tk.Canvas(parent['real_widget'], bg=self['background'].hex,
                           width=width, height=height)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def _bananagui_set_size(self, size):
        width, height = size
        self['real_widget'].config(width=width, height=height)

    def _bananagui_set_background(self, background):
        self['real_widget'].config(bg=background.hex)

    def draw_line(self, pos1, pos2, thickness, color):
        self['real_widget'].create_line(
            *itertools.chain(pos1, pos2),
            fill=color.hex, width=thickness)

    def draw_polygon(self, *positions, fillcolor, linecolor, linethickness):
        if fillcolor is None:
            kwargs = {}
        else:
            kwargs = {'fill': fillcolor.hex}
        self['real_widget'].create_polygon(
            *itertools.chain.from_iterable(positions),
            outline=linecolor.hex, width=linethickness, **kwargs)

    def draw_oval(self, centerpos, xradius, yradius, fillcolor,
                  linecolor, linethickness):
        centerx, centery = centerpos
        if fillcolor is None:
            kwargs = {}
        else:
            kwargs = {'fill': fillcolor.hex}
        self['real_widget'].create_oval(
            centerx - xradius, centery - yradius,
            centerx + xradius, centery + yradius,
            outline=linecolor.hex, width=linethickness, **kwargs)
