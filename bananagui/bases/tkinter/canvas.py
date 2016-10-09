import itertools
import tkinter as tk


class Canvas:

    def __init__(self, parent, **kwargs):
        width, height = self['size']
        widget = tk.Canvas(parent['real_widget'], bg=self['background'].hex,
                           width=width, height=height)
        widget.bind('<Configure>', self.__configure)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def __configure(self, event):
        self.size.raw_set((event.width, event.height))

    def _bananagui_set_minimum_size(self, size):
        width, height = size
        self['real_widget'].config(width=width, height=height)

    def _bananagui_set_background(self, background):
        self['real_widget'].config(bg=background.hex)

    def draw_line(self, start, end, thickness, color):
        self['real_widget'].create_line(
            # *start, *end doesn't work on Pythons older than 3.5.
            *itertools.chain(start, end),
            fill=color.hex, width=thickness)

    def draw_polygon(self, *corners, fillcolor, linecolor, linethickness):
        kwargs = {}
        if fillcolor is not None:
            kwargs['fill'] = fillcolor.hex
        if linecolor is not None:
            kwargs['outline'] = linecolor.hex
        self['real_widget'].create_polygon(
            *itertools.chain.from_iterable(corners),
            width=linethickness, **kwargs)

    def draw_oval(self, center, xradius, yradius, fillcolor,
                  linecolor, linethickness):
        centerx, centery = center
        kwargs = {}
        if fillcolor is not None:
            kwargs['fill'] = fillcolor.hex
        if linecolor is not None:
            kwargs['outline'] = linecolor.hex
        self['real_widget'].create_oval(
            centerx - xradius, centery - yradius,
            centerx + xradius, centery + yradius,
            width=linethickness, **kwargs)
