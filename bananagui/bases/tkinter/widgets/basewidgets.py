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


class _Tooltip:
    """Tooltips for tkinter.

    License notice: This class has nothing to do with idlelib.ToolTip. I
    didn't copy-paste this from idlelib and I didn't read idlelib's
    tooltip.py when I wrote this. I wrote my own tooltip manager mainly
    because I didn't have the time to find out how I'm allowed to use
    idlelib's code.
    """

    # This needs to be shared by all instances because there's only one
    # mouse pointer.
    tipwindow = None

    def __init__(self, widget):
        widget.bind('<Enter>', self.enter)
        widget.bind('<Leave>', self.leave)
        widget.bind('<Motion>', self.motion)
        self.widget = widget
        self.got_mouse = False
        self.content = None

    @classmethod
    def destroy_tipwindow(cls, event=None):
        if cls.tipwindow is not None:
            cls.tipwindow.destroy()
            cls.tipwindow = None

    def enter(self, event):
        if event.widget is not self.widget:
            # For some reason, toplevels get also notified of their
            # childrens' events.
            return
        self.destroy_tipwindow()
        self.got_mouse = True
        event.widget.after(1000, self.show)

    def leave(self, event):
        if event.widget is not self.widget:
            return
        self.destroy_tipwindow()
        self.got_mouse = False

    def motion(self, event):
        self.mousex = event.x_root
        self.mousey = event.y_root

    def show(self):
        if not self.got_mouse:
            return
        self.destroy_tipwindow()
        if self.content is not None:
            tipwindow = type(self).tipwindow = tk.Toplevel()
            tipwindow.geometry('+%d+%d' % (self.mousex+10, self.mousey-10))
            tipwindow.bind('<Motion>', self.destroy_tipwindow)
            tipwindow.overrideredirect(True)

            # If you modify this, make sure to always define either no
            # colors at all or both foreground and background. Otherwise
            # the label will have light text on a light background or
            # dark text on a dark background on some systems.
            label = tk.Label(tipwindow, text=self.content, border=3,
                             fg='black', bg='white')
            label.pack()


_expand_indexes = {
    bananagui.HORIZONTAL: 0,
    bananagui.VERTICAL: 1,
}


class Widget:

    def __init__(self, bananawidget):
        self.bananawidget = bananawidget

    def focus(self):
        self.real_widget.focus()


class Child(Widget):

    def __init__(self, bananawidget, parent):
        self._packed = False  # See also containers.py.
        self.parent = parent
        super().__init__(bananawidget)
        self._tooltip = _Tooltip(self.real_widget)

    def set_expand(self, expand):
        if self._packed:
            # Update the pack expanding. By having this here we can make
            # sure that the pack options are changed when the expand is
            # changed.
            pack_kwargs = {'fill': tkinter_fills[expand]}
            try:
                # Maybe it's a Box and we can use its orientation?
                index = _expand_indexes[self.parent.orientation]
                pack_kwargs['expand'] = expand[index]
            except AttributeError:
                # It's not a box. We need a default value.
                pack_kwargs['expand'] = (expand == (True, True))
            self.real_widget.pack(**pack_kwargs)

    def set_tooltip(self, tooltip):
        self._tooltip.content = tooltip

    def set_grayed_out(self, grayed_out):
        self.real_widget['state'] = 'disable' if grayed_out else 'normal'
