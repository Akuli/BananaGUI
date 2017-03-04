from tkinter import colorchooser
from . import mainloop


def colordialog(parentwindow, color, title):
    rgb, hexcolor = colorchooser.askcolor(
        color, title=title, parent=parentwindow.real_widget)

    # The RGB color doesn't seem to work right, I'm getting
    # (255.99609375, 255.99609375, 255.99609375) when the hexcolor
    # is '#ffffff'.
    if hexcolor is not None:
        hexcolor = mainloop._convert_color(hexcolor)
    return hexcolor
