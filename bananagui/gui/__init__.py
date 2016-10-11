"""The actual BananaGUI widgets.

Call bananagui.load() before importing this.
"""

# flake8: noqa

import bananagui

if bananagui._base is None:
    raise ImportError("call bananagui.load() before importing bananagui.gui")

from .bases import Widget, Parent, Child
from .buttons import BaseButton, Button, ImageButton
from .canvas import Canvas
from .containers import Bin, Box
from .labels import BaseLabel, Label, ImageLabel
from .mainloop import init, main, quit
from .misc import Checkbox, Dummy, Separator, Spinner
from .textwidgets import TextBase, Entry, PlainTextView
from .trayicon import TrayIcon

# Bases don't need to provide infodialog, questiondialog, warningdialog
# or errordialog. See windows.py for more info.
from .windows import (
    BaseWindow, Window, Dialog, messagedialog,
    infodialog, questiondialog, warningdialog, errordialog)

# Some things in this module aren't actually GUI widgets but other
# things that GUI toolkits like to provide.
from .clipboard import set_clipboard_text, get_clipboard_text
from .timeouts import add_timeout

# Initialize the GUI.
init()
