"""The actual BananaGUI widgets.

Call bananagui.load() before importing this.
"""

# flake8: noqa

import bananagui
if bananagui._base is None:
    raise ImportError("call bananagui.load() before importing bananagui.gui")

from .bases import Widget, Parent, Child, Oriented, Ranged
from .buttons import BaseButton, Button, ImageButton
from .canvas import Canvas
from .clipboard import set_clipboard_text, get_clipboard_text
from .containers import Bin, Box
from .dialogs import (Dialog, infodialog, questiondialog, warningdialog,
                      errordialog, colordialog, fontdialog)
from .labels import BaseLabel, Label, ImageLabel
from .mainloop import init, main, quit
from .misc import (Checkbox, Dummy, Separator, Spinner, Spinbox, Slider,
                   Progressbar, get_font_families)
from .textwidgets import TextBase, Entry, PlainTextView
from .timeouts import add_timeout
from .trayicon import TrayIcon
from .window import BaseWindow, Window

# Initialize the GUI so people don't need to call gui.init() after
# importing it.
init()
