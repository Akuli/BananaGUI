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

import functools
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


def run_when_ready(method):
    @functools.wraps(method)
    def inner(self, *args, **kwargs):
        if (not isinstance(self, Child)) or self.todo is None:
            # We have a widget and we can just run this.
            return method(self, *args, **kwargs)
        # We need to do this later. Unfortunately we don't get a return
        # value this way, which might be a problem in some cases...
        partial = functools.partial(method, self, *args, **kwargs)
        self.todo.append(partial)
        return None

    return inner


class Widget:

    def __init__(self, bananawidget):
        self.bananawidget = bananawidget

    def focus(self):
        self.real_widget.focus()


class Parent(Widget):

    def __init__(self, bananawidget):
        # This is for compatibility with run_when_ready().
        if not hasattr(self, 'parent'):
            self.parent = None
        super().__init__(bananawidget)

    def create(self, parent):
        # self can be a subclass of Child, and there's no guarantees
        # about which order Parent and Child appear in the mro. Window
        # and Dialog objects also have this method, but it's never
        # called.
        if hasattr(super(), 'create'):
            # It's a Child, not a Window or Dialog.
            assert parent is not None
            super().create(parent)
        for child in self.bananawidget.iter_children():
            child._wrapper.create(self)

    def _prepare_add(self, child):
        """Prepare a child for being added to this widget."""
        child._packed = True
        if child.real_widget is None:
            child.create(self)

    def _prepare_remove(self, child):
        """Prepare a child for being removed from this widget."""
        child._packed = False


class Child(Widget):
    # This is a bit tricky because tkinter widgets need to know their
    # parent when they are created. There's a create method that
    # creates the widgets when their parents are known all the way to
    # the top window. It calls everything in the todo list with no
    # arguments. The run_when_ready decorator can be used for
    # automatically adding a partial to the todo list instead of trying
    # to run the function. The todo list is set to None when the widget
    # has been created.

    def __init__(self, bananawidget):
        self.todo = []
        self.parent = None
        self._packed = False  # See also containers.py.
        self.real_widget = None
        super().__init__(bananawidget)

    def create(self, parent):
        # Subclasses should provide a create_widget method.
        if self.todo is None:
            # It has been created already.
            return
        self.parent = parent
        self.real_widget = self.create_widget(self.parent)
        self._tooltip = _Tooltip(self.real_widget)
        for thing in self.todo:
            thing()
        self.todo = None
        if hasattr(super(), 'create'):
            # Run Parent.create. See its documentation for more info.
            super().create(parent)

    @run_when_ready
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

    @run_when_ready
    def set_tooltip(self, tooltip):
        self._tooltip.content = tooltip

    @run_when_ready
    def set_grayed_out(self, grayed_out):
        self.real_widget['state'] = 'disable' if grayed_out else 'normal'
