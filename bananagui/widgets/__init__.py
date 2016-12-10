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

"""The actual BananaGUI widgets."""

# flake8: noqa


def _fix_modules(names):
    """Make classes and functions seem like they come from here."""
    for name in names:
        class_or_func = globals()[name]
        class_or_func.__module__ = __name__


_old_dir = set(dir())

from .basewidgets import Widget, Parent, Child
from .buttons import BaseButton, Button, ImageButton
from .containers import Bin, Box, Scroller
from .labels import BaseLabel, Label, ImageLabel
from .misc import (Checkbox, Dummy, Separator, set_clipboard_text,
                   get_clipboard_text)
from .progress import Progressbar, BouncingProgressbar, Spinner
from .ranged import Slider, Spinbox
from .textwidgets import TextBase, Entry, TextEdit
#from .trayicon import TrayIcon
from .window import BaseWindow, Window, Dialog

_fix_modules(set(dir()) - _old_dir - {'_old_dir'})
