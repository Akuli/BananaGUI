# Copyright (c) 2016 Akuli

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
from .containers import Bin, Box, Scroller
from .labels import BaseLabel, Label, ImageLabel
from .mainloop import init, main, quit, add_timeout
from .misc import (Checkbox, Dummy, Separator, set_clipboard_text,
                   get_clipboard_text, get_font_families)
from .progress import Progressbar, BouncingProgressbar
from .ranged import Slider, Spinbox
from .textwidgets import TextBase, Entry, PlainTextView
from .trayicon import TrayIcon
from .window import BaseWindow, Window, Dialog, colordialog
