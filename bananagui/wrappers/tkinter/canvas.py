import tkinter as tk

from bananagui import color as _color


def _flatten(iterables):
    for iterable in iterables:
        # yield from is new in Python 3.3.
        for item in iterable:
            yield item


class Canvas:

    def __init__(self, parent):
        super().__init__(parent)
        widget = tk.Canvas(parent['real_widget'], width=300, height=200,
                           bg='#ffffff')
        self.raw_set('real_widget', widget)

    def _bananagui_set_size(self, size):
        width, height = size
        self['real_widget'].config(width=width, height=height)

    def _bananagui_set_background(self, background):
        self['real_widget'].config(bg=background.hex)

    def draw_line(self, pos1, pos2, thickness, color):
        self['real_widget'].create_line(*_flatten((pos1, pos2)),
                                        fill=color.hex, width=thickness)

    def draw_polygon(self, *positions, fillcolor, linecolor, linethickness):
        if fillcolor is None:
            kwargs = {}
        else:
            kwargs = {'fill': fillcolor.hex}
        self['real_widget'].create_polygon(
            *_flatten(positions), outline=linecolor.hex,
            width=linethickness, **kwargs)

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
