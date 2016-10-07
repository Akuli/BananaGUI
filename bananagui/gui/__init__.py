"""The actual BananaGUI widgets.

Call bananagui.load() before importing this.
"""

# flake8: noqa

import bananagui

if bananagui._base is None:
    raise ImportError("call bananagui.load() before importing bananagui.gui")

from .bases import Widget, Parent, Child, Dummy
from .buttons import BaseButton, Button
from .canvas import Canvas
from .checkbox import Checkbox
from .containers import Bin, Box, HBox, VBox
from .labels import BaseLabel, Label, ImageLabel
from .mainloop import init, main, quit
from .textwidgets import TextBase, Entry, PlainTextView

# Bases don't need to provide infodialog, questiondialog, warningdialog
# or errordialog. See windows.py for more info.
from .windows import (
    BaseWindow, Window, Dialog, messagedialog,
    infodialog, questiondialog, warningdialog, errordialog)

# Some things in this module aren't actually GUI widgets but other
# things that GUI toolkits like to provide.
#from .clipboard import Clipboard
from .timeouts import RUN_AGAIN, add_timeout

# Initialize the GUI.
init()
