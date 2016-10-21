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

import bananagui
from . import tkinter_fills
from .containers import Box


class _Tooltip:
    """Tooltips for tkinter.

    License notice: This class has nothing to do with idlelib.ToolTip. I
    didn't copy-paste this from idlelib and I didn't read idlelib's
    tooltip.py when I wrote this. I wrote my own tooltip manager mainly
    because I didn't have the time to find out how I'm allowed to use
    idlelib's code.
    """

    # This should never contain more than one window at a time, but we
    # allow multiple windows to make sure nothing breaks if we have
    # multiple tipwindows at the same time for some reason.
    _tipwindows = set()

    def __init__(self, widget, content=None):
        widget.bind('<Enter>', self._enter)
        widget.bind('<Leave>', self._leave)
        widget.bind('<Motion>', self._motion)
        self._widget = widget
        self._got_mouse = False
        self.content = content

    def _destroy_tipwindows(self, event=None):
        while self._tipwindows:
            tipwindow = self._tipwindows.pop()
            tipwindow.destroy()

    def _enter(self, event):
        if event.widget is not self._widget:
            # For some reason, toplevels get also notified of their
            # childrens' events.
            return
        self._destroy_tipwindows()
        self._got_mouse = True
        event.widget.after(1000, self._show)

    def _leave(self, event):
        if event.widget is not self._widget:
            return
        self._destroy_tipwindows()
        self._got_mouse = False

    def _motion(self, event):
        self._mousex = event.x_root
        self._mousey = event.y_root

    def _show(self):
        if not self._got_mouse:
            return
        self._destroy_tipwindows()
        if self.content is not None:
            tipwindow = tk.Toplevel()
            tipwindow.geometry('+%d+%d' % (self._mousex+10, self._mousey-10))
            tipwindow.bind('<Motion>', self._destroy_tipwindows)
            tipwindow.overrideredirect(True)
            self._tipwindows.add(tipwindow)

            # If you modify this, make sure to always define either no
            # colors at all or both foreground and background. Otherwise
            # the label will have light text on a light background or
            # dark text on a dark background on some systems.
            label = tk.Label(tipwindow, text=self.content,
                             fg='black', bg='white')
            label.pack()


class Widget:
    pass


class Parent:
    pass


_expand_indexes = {
    bananagui.HORIZONTAL: 0,
    bananagui.VERTICAL: 1,
}


class Child:

    def __init__(self, **kwargs):
        self.__tooltip = _Tooltip(self['real_widget'])
        self._bananagui_tkinter_packed = False  # See also containers.py.
        super().__init__(**kwargs)

    def _bananagui_set_expand(self, expand):
        if self._bananagui_tkinter_packed:
            # Update the pack expanding. By having this here we can make
            # sure that the pack options are changed when the expand is
            # changed.
            pack_kwargs = {'fill': tkinter_fills[expand]}
            if isinstance(self['parent'], Box):
                index = _expand_indexes[self['parent']['orientation']]
                pack_kwargs['expand'] = expand[index]
            else:
                # It's not a box. We need a default value.
                pack_kwargs['expand'] = (expand == (True, True))
            self['real_widget'].pack(**pack_kwargs)

    def _bananagui_set_tooltip(self, tooltip):
        self.__tooltip.content = tooltip

    def _bananagui_set_grayed_out(self, grayed_out):
        self['real_widget']['state'] = 'disable' if grayed_out else 'normal'
