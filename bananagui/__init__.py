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
the same code using any of the supported GUI toolkits, including PyQt 5,
GTK+ 3 and tkinter.
"""

import importlib
import types

# The bananagui.wrappers module is needed for relative imports in
# load_guiwrapper.
from bananagui import base, core, gui, wrappers  # noqa


BLACK = '#000000'
GRAY = '#7f7f7f'
WHITE = '#ffffff'
RED = '#ff0000'
ORANGE = '#ff7f00'
YELLOW = '#ffff00'
GREEN = '#00ff00'
CYAN = '#00ffff'
BLUE = '#0000ff'
PINK = '#ff00ff'


def load_guiwrapper(*wrappers):
    """Load a BananaGUI wrapper module into bananagui.gui.

    The wrappers can be Python modules or module names. If they are
    relative names, they will be treated as relative to
    bananagui.wrappers. For example, '.tkinter' is equivalent to
    'bananagui.wrappers.tkinter'.

    If multiple wrappers are given, attempt to load each one until
    loading one of them succeeds.
    """
    if not wrappers:
        raise ValueError("specify at least one wrapper")

    if len(wrappers) == 1:
        # Load the wrapper.
        wrapper = wrappers[0]
        if not isinstance(wrapper, types.ModuleType):
            wrapper = importlib.import_module(wrapper, 'bananagui.wrappers')
        core.load_wrapper(base, wrapper)
    else:
        # Attempt to load each wrapper.
        for wrapper in wrappers:
            try:
                load_guiwrapper(wrapper)
                return
            except ImportError:
                pass
        raise ImportError("cannot load any of the requested GUI wrappers")
