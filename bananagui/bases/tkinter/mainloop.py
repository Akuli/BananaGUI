import tkinter as tk

import bananagui


root = None


def init():
    global root
    root = tk.Tk()
    root.withdraw()


def main():
    root.mainloop()


def quit():
    global root
    root.destroy()
    root = None


def convert_color(colorstring):
    """Convert a tkinter color string to a BananaGUI color.

    Unlike bananagui.Color.from_hex, this also handles color names like
    'red'.
    """
    # I have no idea why the biggest value is 65535. To scale it down to
    # 255 we need to divide it by 65535/255=257.
    rgb = [value // 257 for value in root.winfo_rgb(colorstring)]
    return bananagui.Color(*rgb)
