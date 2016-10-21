"""BananaGUI tkinter base."""
# flake8: noqa

import bananagui

tkinter_orients = {
    bananagui.HORIZONTAL: 'horizontal',
    bananagui.VERTICAL: 'vertical',
}
tkinter_fills = {
    # BananaGUI expand: tkinter's fill option, ...
    (True, True): 'both',
    (True, False): 'x',
    (False, True): 'y',
    (False, False): 'none',
}

from .basewidgets import Widget, Parent, Child
from .buttons import BaseButton, Button, ImageButton
from .canvas import Canvas
from .containers import Bin, Box
from .labels import BaseLabel, Label, ImageLabel
from .mainloop import init, main, quit, add_timeout
from .misc import (Checkbox, Dummy, Separator, set_clipboard_text,
                   get_clipboard_text, get_font_families)
from .progress import Progressbar, BouncingProgressbar
from .ranged import Slider, Spinbox
from .textwidgets import TextBase, Entry, PlainTextView
from .trayicon import TrayIcon
from .window import BaseWindow, Window, Dialog, colordialog
