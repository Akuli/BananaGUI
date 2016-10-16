import tkinter as tk

from . import mainloop


class BaseWindow:

    def __init__(self, **kwargs):
        widget = self['real_widget']
        widget.title(self['title'])
        widget.bind('<Configure>', self.__configure)
        widget.protocol('WM_DELETE_WINDOW', self.__delete_window)
        super().__init__(**kwargs)

    def __configure(self, event):
        self.size.raw_set((event.width, event.height))

    def __delete_window(self):
        self.on_destroy.emit()

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
