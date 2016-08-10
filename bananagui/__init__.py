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

"""Simple wrapper for GUI frameworks.

To get started with using BananaGUI, get a GUI toolkit wrapper with the
get() function. For example, gui = bananagui.get('tkinter'). The
wrappers come from bananagui.wrappers, so you can go there to see which
wrappers BananaGUI comes with.
"""

import importlib
import re

from bananagui.core.structures import Font   # noqa


HORIZONTAL = 'h'
VERTICAL = 'v'

RED = Color(255, 0, 0)
ORANGE = Color(255, 127, 0)
YELLOW = Color(255, 255, 0)
GREEN = Color(0, 255, 0)
CYAN = Color(0, 255, 255)
BLUE = Color(0, 0, 255)
PINK = Color(255, 0, 255)
BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)

GRAY50 = BLACK + WHITE
GRAY25 = GRAY50 + BLACK
GRAY75 = GRAY50 + WHITE


class MissingFeatureWarning(UserWarning):
    """Warned when a GUI toolkit doesn't have the requested feature."""


class PropertyError(AttributeError):
    """Raised when a property related problem is detected.

    Usually the property is not found, or the property doesn't have the
    requested setter or getter.
    """


def get(*toolkit_names):
    """Attempt to return a GUI toolkit wrapper from toolkit_names.

    The first one is imported and returned, and if it's not avaliable
    the next one is, and so on.
    """
    if not toolkit_names:
        raise ValueError("no toolkit names were given")
    for name in toolkit_names:
        try:
            return importlib.import_module('bananagui.wrappers.' + name)
        except ImportError:
            pass
    raise ImportError("cannot import any of the requested toolkits")
