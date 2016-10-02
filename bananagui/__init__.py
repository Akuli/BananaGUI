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

import importlib

# This is imported because importlib.import_module() doesn't import
# parent modules as needed with relative imports.
import bananagui.bases  # noqa


_base = None


def load(*args):
    """Load bananagui.gui.

    The arguments should be Python module names. If they are relative,
    they will be treated as relative to bananagui.bases. For example,
    '.tkinter' is equivalent to 'bananagui.bases.tkinter'.

    If multiple wrappers are given, attempt to load each one until
    loading one of them succeeds. You can import `bananagui.gui` after
    calling this.
    """
    if not args:
        raise ValueError("specify at least one wrapper")

    if len(args) == 1:
        # Load the wrapper.
        global _base
        if _base is not None:
            raise RuntimeError("don't call bananagui.load() twice")
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
