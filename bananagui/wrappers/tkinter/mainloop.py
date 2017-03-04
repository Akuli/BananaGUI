import tkinter as tk

import bananagui
from bananagui import color

root = None    # Make flake8 happy.


def init():
    global root
    root = tk.Tk()
    root.withdraw()


def run():
    root.mainloop()


def quit():
    root.destroy()


def add_timeout(milliseconds, callback):
    after = root.after

    def real_callback():
        if callback() == bananagui.RUN_AGAIN:
            after(milliseconds, real_callback)

    after(milliseconds, real_callback)


def _convert_color(colorstring):
    """Convert a tkinter color string to a hexadecimal color.

    Tkinter colors are usually hexadecimal, but this function also
    handles color names like 'red' or 'SystemDefault'.
    """
    # Tkinter uses 65535 as the maximum value. We need to divide the
    # values by 65535//255=257.
    rgb = (value // 257 for value in root.winfo_rgb(colorstring))
    return color.rgb2hex(rgb)
