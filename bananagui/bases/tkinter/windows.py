import tkinter as tk

from . import mainloop


class WindowBase:

    def __init__(self):
        super().__init__()
        self['real_widget'].title(self['title'])
        self['real_widget'].bind('<<Configure>>', print)  # TODO
        self['real_widget'].protocol('WM_DELETE_WINDOW', self.destroy)

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

    def destroy(self):
        try:
            self['real_widget'].destroy()
        except tk.TclError:
            # The widget has already been destroyed.
            pass


class Window:

    def __init__(self):
        # This relies on tkinter's default root, which is created in the
        # mainloop.py file.
        widget = tk.Toplevel(mainloop.root)
        self.real_widget.raw_set(widget)
        super().__init__()


class Dialog:

    def __init__(self, parentwindow):
        widget = tk.Toplevel(parentwindow['real_widget'])
        self.real_widget.raw_set(widget)
        super().__init__(parentwindow)


def messagedialog(icon, parentwindow, text, title, buttons, defaultbutton):
    raise NotImplementedError  # TODO
