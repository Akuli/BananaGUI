import functools
import tkinter as tk

from bananagui import Orient
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
        self.widget.focus()


_expand_indexes = {
    Orient.HORIZONTAL: 0,
    Orient.VERTICAL: 1,
}


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
        self._packed = False  # See also parents.py.
        self.widget = None
        super().__init__(bananawidget)

    def create(self, parent):
        # Subclasses should provide a create_widget method.
        if self.todo is None:
            # It has been created already.
            return
        self.parent = parent
        self.widget = self.create_widget(self.parent)
        self._tooltip = _Tooltip(self.widget)
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
            self.widget.pack(**pack_kwargs)

    @run_when_ready
    def set_tooltip(self, tooltip):
        self._tooltip.content = tooltip

    @run_when_ready
    def set_grayed_out(self, grayed_out):
        self.widget['state'] = 'disable' if grayed_out else 'normal'

    focus = run_when_ready(Widget.focus)
