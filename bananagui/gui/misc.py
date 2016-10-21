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

import bananagui
from bananagui import _base
from .basewidgets import Oriented, Child

# TODO: A RadioButton, or _RadioButton and RadioButtonManager.


@bananagui.bananadoc
class Checkbox(_base.Checkbox, Child):
    """A widget that can be checked.

    The Checkbox widget has nothing to do with the Box widget.
    """

    text = bananagui.Property(
        'text', type=str, default='',
        doc="The text next to the box that can be checked.")
    checked = bananagui.Property(
        'checked', type=bool, default=False,
        doc="True if the box is currently checked, False if not.")


@bananagui.bananadoc
class Dummy(_base.Dummy, Child):
    """An empty widget.

    This is useful for creating layouts with empty space that must be
    filled with something.
    """


@bananagui.bananadoc
class Separator(Oriented, _base.Separator, Child):
    """A horizontal or vertical line."""

    def __init__(self, parent, **kwargs):
        # Make the separator expand correctly by default.
        orientation = kwargs.get('orientation')
        if orientation == bananagui.HORIZONTAL:
            kwargs.setdefault('expand', (True, False))
        if orientation == bananagui.VERTICAL:
            kwargs.setdefault('expand', (False, True))
        super().__init__(parent, **kwargs)


def set_clipboard_text(text: str) -> None:
    """Set text to the clipboard."""
    _base.set_clipboard_text(text)


def get_clipboard_text() -> str:
    """Return the text that is currently on the clipboard."""
    return _base.get_clipboard_text()


def get_font_families() -> list:
    """Return a list of all avaliable font families."""
    # This is converted to a set first to make sure that we don't get
    # any duplicates. The base function can return anything iterable.
    return sorted(set(_base.get_font_families()))
