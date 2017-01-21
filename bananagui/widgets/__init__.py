# Copyright (c) 2016-2017 Akuli

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


def _fix_modulenames():
    """Make classes and functions seem like they come from here.

    Return an __all__ list.
    """
    result = []
    for name, value in globals().items():
        if callable(value) and not name.startswith('_'):
            # public class or function
            result.append(name)
    return result


from .basewidgets import Widget, Child
from .buttons import Button, ImageButton
from .labels import Label, ImageLabel
from .misc import Checkbox, Dummy, Separator
from .parents import Parent, Bin, Box, Scroller, Group
from .progress import Progressbar, BouncingProgressbar, Spinner
from .ranged import Slider, Spinbox
from .textwidgets import TextBase, Entry, TextEdit
#from .trayicon import TrayIcon
from .window import BaseWindow, Window, Dialog

__all__ = _fix_modulenames()
