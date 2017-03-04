import tkinter as tk

from . import mainloop


def set_text(text):
    mainloop.root.clipboard_clear()
    mainloop.root.clipboard_append(text)


def get_text():
    try:
        return mainloop.root.clipboard_get()
    except tk.TclError:
        # There's nothing on the clipboard.
        return None
