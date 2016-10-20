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

"""Checkbox, Separator and Spinner widgets."""

import bananagui
from bananagui import _base
from . import bases

try:
    _SpinnerBase = _base.Spinner
except AttributeError:
    # The base doesn't provide a spinner. We need to create one using
    # other widgets.
    from bananagui.bases.defaults import Spinner as _SpinnerBase

# TODO: A RadioButton, or _RadioButton and RadioButtonManager.


@bananagui.bananadoc
class Checkbox(_base.Checkbox, bases.Child):
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
class Dummy(_base.Dummy, bases.Child):
    """An empty widget.

    This is useful for creating layouts with empty space that must be
    filled with something.
    """


@bananagui.bananadoc
class Separator(bases.Oriented, _base.Separator, bases.Child):
    """A horizontal or vertical line."""

    def __init__(self, parent, **kwargs):
        # Make the separator expand by default.
        orientation = kwargs.get('orientation')
        if orientation == bananagui.HORIZONTAL:
            kwargs.setdefault('expand', (True, False))
        if orientation == bananagui.VERTICAL:
            kwargs.setdefault('expand', (False, True))
        super().__init__(parent, **kwargs)


class Spinner(_SpinnerBase, bases.Child):
    """A waiting spinner.

    The spinner doesn't spin by default. You can set the spinning
    property to True to make it spin.
    """

    spinning = bananagui.Property(
        'spinning', type=bool, default=False,
        doc="True if the widget is currently spinning, False if not.")


class Spinbox(bases.Ranged, _base.Spinbox, bases.Child):
    """A box for selecting a number with arrow buttons up and down."""


class Slider(bases.Oriented, bases.Ranged, _base.Slider, bases.Child):
    """A slider for selecting a number."""


class Progressbar(bases.Oriented, _base.Progressbar, bases.Child):
    """A progress bar widget."""

    progress = bananagui.Property(
        'progress', type=(float, int), minimum=0, maximum=1, default=0,
        doc="The progressbar's position.")


def get_font_families() -> list:
    """Return a list of all avaliable font families."""
    # This is converted to a set first to make sure that we don't get
    # any duplicates. The base function can return anything iterable.
    return sorted(set(_base.get_font_families()))
