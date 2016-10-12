import tkinter as tk
from tkinter import colorchooser

from bananagui import Color


class Dialog:

    def __init__(self, parentwindow, **kwargs):
        widget = tk.Toplevel(parentwindow['real_widget'])
        self.real_widget.raw_set(widget)
        super().__init__(parentwindow, **kwargs)


def messagedialog(icon, parentwindow, text, title, buttons, defaultbutton):
    raise NotImplementedError  # TODO


def colordialog(parentwindow, color, title):
    result = colorchooser.askcolor(
        color.hex, title=title,
        parent=parentwindow['real_widget'])
    if result == (None, None):
        return None
    return Color.from_hex(result[1])
