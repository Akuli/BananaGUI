import tkinter as tk
from tkinter import colorchooser

from . import mainloop


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
