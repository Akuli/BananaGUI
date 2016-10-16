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

from bananagui import _base, bananadoc, Property, HORIZONTAL, VERTICAL
from .bases import Oriented, Ranged, Child

try:
    _SpinnerBase = _base.Spinner
except AttributeError:
    # The base doesn't provide a spinner. We need to create one using
    # other widgets.
    from bananagui.bases.defaults import Spinner as _SpinnerBase

# TODO: A RadioButton, or _RadioButton and RadioButtonManager.


@bananadoc
class Checkbox(_base.Checkbox, Child):
    """A widget that can be checked.

    The Checkbox widget has nothing to do with the Box widget.
    """

    text = Property('text', type=str, default='',
                    doc="The text next to the box that can be checked.")
    checked = Property(
        'checked', type=bool, default=False,
        doc="True if the box is currently checked, False if not.")


@bananadoc
class Dummy(_base.Dummy, Child):
    """An empty widget.

    This is useful for creating layouts with empty space that must be
    filled with something.
    """


@bananadoc
class Separator(Oriented, _base.Separator, Child):
    """A horizontal or vertical line."""

    def __init__(self, parent, **kwargs):
        # Make the separator expand by default.
        orientation = kwargs.get('orientation')
        if orientation == HORIZONTAL:
            kwargs.setdefault('expand', (True, False))
        if orientation == VERTICAL:
            kwargs.setdefault('expand', (False, True))
        super().__init__(parent, **kwargs)


class Spinner(_SpinnerBase, Child):
    """A waiting spinner.

    The spinner doesn't spin by default. You can set the spinning
    property to True to make it spin.
    """

    spinning = Property(
        'spinning', type=bool, default=False,
        doc="True if the widget is currently spinning, False if not.")


class Spinbox(Ranged, _base.Spinbox, Child):
    """A box for selecting a number with arrow buttons up and down."""


class Slider(Oriented, Ranged, _base.Slider, Child):
    """A slider for selecting a number."""


def get_font_families() -> list:
    """Return a list of all avaliable font families."""
    # This is converted to a set first to make sure that we don't get
    # any duplicates. The base function can return anything iterable.
    return sorted(set(_base.get_font_families()))
