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

"""Wrapper module for other GUI toolkits.

With BananaGUI you can write a GUI application in Python, and then run
the same code using any of the supported GUI toolkits, including PyQt5,
GTK+ 3 and tkinter.
"""

# flake8: noqa

import importlib

# This is imported because importlib.import_module() doesn't import
# parent modules as needed with relative imports.
import bananagui.bases

# Importing other things. CallbackList and CallbackDict aren't imported
# here because they're meant to be used internally by BananaGUI.
from bananagui.structures import Color, Font
from bananagui.types import (BananaProperty, Event, BananaSignal,
                             BananaObject, document_props)


# These constants can be used with these variables or with their values
# directly.
HORIZONTAL = 'h'
VERTICAL = 'v'

# This is not 0 or 1 because returning True or False from a callback
# must not be allowed.
RUN_AGAIN = 2

# TODO: Add a BROWN.
BLACK = Color(0, 0, 0)
GRAY = Color(127, 127, 127)
WHITE = Color(255, 255, 255)
RED = Color(255, 0, 0)
ORANGE = Color(255, 127, 0)
YELLOW = Color(255, 255, 0)
GREEN = Color(0, 255, 0)
CYAN = Color(0, 255, 255)
BLUE = Color(0, 0, 255)
PINK = Color(255, 0, 255)


_base = None


def load(*args):
    """Load bananagui.gui.

    The arguments should be Python module names. If they are relative,
    they will be treated as relative to bananagui.bases. For example,
    '.tkinter' is equivalent to 'bananagui.bases.tkinter'.

    If multiple base modules are given, attempt to load each one until
    loading one of them succeeds. You can import bananagui.gui after
    calling this.
    """
    if not args:
        raise ValueError("specify at least one module")

    global _base
    if _base is not None:
        raise RuntimeError("don't call bananagui.load() twice")

    if len(args) == 1:
        # Load the base.
        _base = importlib.import_module(args[0], 'bananagui.bases')

    else:
        # Attempt to load each base.
        for arg in args:
            try:
                load(arg)
                return
            except ImportError:
                pass
        raise ImportError("cannot load any of the requested base modules")

    from bananagui import gui
    gui.init()
