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

import tkinter as tk

from bananagui import HORIZONTAL, VERTICAL
from .containers import Box


class _TooltipBase:
    """Tooltips for tkinter.

    This has nothing to do with idlelib.ToolTip. I didn't copy-paste
    this from idlelib and I didn't read idlelib's tooltip.py when I
    wrote this.
    """

    # This should never contain more than one window at a time, but we
    # allow multiple windows to make sure nothing breaks if we have
    # multiple tipwindows at the same time for some reason.
    __tipwindows = set()

    def __init__(self, *args, **kwargs):
        self.__got_mouse = False
        self['real_widget'].bind('<Enter>', self.__enter)
        self['real_widget'].bind('<Leave>', self.__leave)
        self['real_widget'].bind('<Motion>', self.__motion)
        super().__init__(*args, **kwargs)

    def __destroy_tipwindows(self, event=None):
        while self.__tipwindows:
            tipwindow = self.__tipwindows.pop()
            tipwindow.destroy()

    def __enter(self, event):
        if event.widget is not self['real_widget']:
            # For some reason, toplevels get also notified of their
            # childrens' events.
            return
        self.__destroy_tipwindows()
        self.__got_mouse = True
        event.widget.after(1000, self.__show)

    def __leave(self, event):
        if event.widget is not self['real_widget']:
            return
        self.__destroy_tipwindows()
        self.__got_mouse = False

    def __motion(self, event):
        self.__mousex = event.x_root
        self.__mousey = event.y_root

    def __show(self):
        if not self.__got_mouse:
            return
        self.__destroy_tipwindows()
        if self['tooltip'] is not None:
            tipwindow = tk.Toplevel()
            tipwindow.geometry('+%d+%d' % (self.__mousex+10, self.__mousey-10))
            tipwindow.bind('<Motion>', self.__destroy_tipwindows)
            tipwindow.overrideredirect(True)
            self.__tipwindows.add(tipwindow)

            # If you modify this, make sure to always define either no
            # colors at all or both foreground and background. Otherwise
            # the label will have light text on a light background or
            # dark text on a dark background on some systems.
            label = tk.Label(tipwindow, text=self['tooltip'],
                             fg='black', bg='white')
            label.pack()

    def _bananagui_set_tooltip(self, tooltip):
        # This needs to be defined, but it doesn't need to do anything
        # because the new tooltip is avaliable as self['tooltip'].
        pass


class Widget:
    pass


class Parent:
    pass


_tkinter_fills = {
    (True, True): 'both',
    (True, False): 'x',
    (False, True): 'y',
    (False, False): 'none',
}
_expand_indexes = {
    HORIZONTAL: 0,
    VERTICAL: 1,
}


class Child(_TooltipBase):

    def __init__(self, **kwargs):
        self._bananagui_tkinter_packed = False  # See also layouts.py.
        super().__init__(**kwargs)

    def _bananagui_set_expand(self, expand):
        if self._bananagui_tkinter_packed:
            # Update the pack expanding. By having this here we can make
            # sure that the pack options are changed when the expand is
            # changed.
            pack_kwargs = {'fill': _tkinter_fills[expand]}
            if isinstance(self['parent'], Box):
                index = _expand_indexes[self['parent']['orientation']]
                pack_kwargs['expand'] = expand[index]
            else:
                # It's not a box. We need a default value.
                pack_kwargs['expand'] = (expand == (True, True))
            self['real_widget'].pack(**pack_kwargs)

    def _bananagui_set_grayed_out(self, grayed_out):
        self['real_widget']['state'] = 'disable' if grayed_out else 'normal'
