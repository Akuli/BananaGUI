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

"""Layout widgets."""

import tkinter as tk


class BoxBase:

    def __init__(self, parent):
        super().__init__(parent)
        self.raw_set('real_widget', tk.Frame(parent['real_widget']))

    def __get_pack_kwargs(self, startorend, expand):
        sides = {
            # (orientation, startorend): side
            ('h', 'start'): 'left',
            ('h', 'end'): 'right',
            ('v', 'start'): 'top',
            ('v', 'end'): 'bottom',
        }
        fills = {
            # (orientation, expand): fill
            ('h', True): 'both',
            ('v', True): 'both',
            ('h', False): 'y',
            ('v', False): 'x',
        }

        orientation = type(self)._bananagui_tkinter_orientation
        return {
            'side': sides[(orientation, startorend)],
            'fill': fills[(orientation, expand)],
            'expand': expand,
        }

    def add_start(self, child, expand):
        kwargs = self.__get_pack_kwargs('start', expand)
        child['real_widget'].pack(**kwargs)

    def add_end(self, child, expand):
        kwargs = self.__get_pack_kwargs('end', expand)
        child['real_widget'].pack(**kwargs)

    def remove(self, child):
        child['real_widget'].pack_forget()


class HBox:
    _bananagui_tkinter_orientation = 'h'


class VBox:
    _bananagui_tkinter_orientation = 'v'
