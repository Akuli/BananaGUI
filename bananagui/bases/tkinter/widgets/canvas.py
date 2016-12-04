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
        width, height = self.minimum_size
        self.real_widget = tk.Canvas(parent.real_widget,
                                     width=width, height=height)
        self.real_widget.bind('<Configure>', self._tkinter_configure)
        super().__init__(parent, **kwargs)

    def _tkinter_configure(self, event):
        self.current_size = (event.width, event.height)

    def _set_minimum_size(self, size):
        width, height = size
        self.real_widget.config(width=width, height=height)

    def draw_line(self, start, end, thickness, color):
        self.real_widget.create_line(*(start + end), fill=color,
                                     width=thickness)

    def draw_polygon(self, *corners, fillcolor, linecolor, linethickness):
        kwargs = {'width': linethickness}
        if fillcolor is not None:
            kwargs['fill'] = fillcolor
        if linecolor is not None:
            kwargs['outline'] = linecolor
        self.real_widget.create_polygon(
            *itertools.chain.from_iterable(corners), **kwargs)

    def draw_oval(self, center, xradius, yradius, fillcolor,
                  linecolor, linethickness):
        centerx, centery = center
        kwargs = {}
        if fillcolor is not None:
            kwargs['fill'] = fillcolor
        if linecolor is not None:
            kwargs['outline'] = linecolor
        self.real_widget.create_oval(
            centerx - xradius, centery - yradius,
            centerx + xradius, centery + yradius,
            width=linethickness, **kwargs)

    def clear(self):
        self.real_widget.delete('all')
