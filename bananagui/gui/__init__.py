"""The actual BananaGUI widgets.

Call bananagui.load() before importing this.
"""

# flake8: noqa

import bananagui
if bananagui._base is None:
    raise ImportError("call bananagui.load() before importing bananagui.gui")

from .basewidgets import Widget, Parent, Child, Oriented, Ranged
from .buttons import BaseButton, Button, ImageButton
from .canvas import Canvas
from .containers import Bin, Box
from .labels import BaseLabel, Label, ImageLabel
from .mainloop import init, main, quit, add_timeout
from .misc import (Checkbox, Dummy, Separator, set_clipboard_text,
                   get_clipboard_text, get_font_families)
from .progress import Progressbar, BouncingProgressbar, Spinner
from .ranged import Slider, Spinbox
from .textwidgets import TextBase, Entry, PlainTextView  # 2DO:rename2TextView?
from .trayicon import TrayIcon
from .window import (BaseWindow, Window, Dialog, infodialog, warningdialog,
                     errordialog, questiondialog, colordialog, fontdialog)

# Initialize the GUI so people don't need to call gui.init() after
# importing it.
init()
