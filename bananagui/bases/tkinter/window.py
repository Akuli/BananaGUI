import tkinter as tk
from tkinter import colorchooser

from . import mainloop


class BaseWindow:

    def __init__(self, **kwargs):
        widget = self['real_widget']
        widget.title(self['title'])
        widget.bind('<Configure>', self.__configure)
        widget.protocol('WM_DELETE_WINDOW', self.on_destroy.emit)
        super().__init__(**kwargs)

    def __configure(self, event):
        self.size.raw_set((event.width, event.height))

    def _bananagui_set_title(self, title):
        self['real_widget'].title(title)

    def _bananagui_set_resizable(self, resizable):
        self['real_widget'].resizable(resizable, resizable)

    def _bananagui_set_size(self, size):
        self['real_widget'].geometry('%dx%d' % size)

    def _bananagui_set_minimum_size(self, size):
        if size is None:
            # Default minimum size.
            size = (1, 1)
        self['real_widget'].minsize(*size)

    def _bananagui_set_showing(self, showing):
        if showing:
            self['real_widget'].deiconify()
        else:
            self['real_widget'].withdraw()

    def wait(self):
        self['real_widget'].wait_window()

    def destroy(self):
        try:
            self['real_widget'].destroy()
        except tk.TclError:
            # The widget has already been destroyed.
            pass


class Window:

    def __init__(self, **kwargs):
        widget = tk.Toplevel(mainloop.root)
        self.real_widget.raw_set(widget)
        super().__init__(**kwargs)


class Dialog:

    def __init__(self, parentwindow, **kwargs):
        widget = tk.Toplevel(parentwindow['real_widget'])
        self.real_widget.raw_set(widget)
        super().__init__(**kwargs)


def colordialog(parentwindow, color, title):
    result = colorchooser.askcolor(
        color.hex, title=title,
        parent=parentwindow['real_widget'])
    if result == (None, None):
        return None
    return mainloop.convert_color(result[1])
