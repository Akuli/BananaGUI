# Copyright (c) 2016 Akuli

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
