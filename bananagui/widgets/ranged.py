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

"""Widgets that have a value that needs to be in a range."""

import bananagui
from bananagui import utils
from .basewidgets import Child, _Oriented

_base = bananagui._get_base('widgets.ranged')


@utils.add_property('value', add_changed=True)
class __Ranged:
    """Implement valuerange and value BananaGUI properties.

    Attributes:
      valuerange        The value range set on initialization.
      value             The widget's current value.
                        This needs to be in valuerange and it's the
                        smallest value of valuerange by default.
      on_value_changed  List of callbacks that are ran when value changes.
    """

    def __init__(self, *args, valuerange=range(11), **kwargs):
        assert isinstance(valuerange, range)
        assert len(valuerange) >= 2
        assert utils.rangestep(valuerange) > 0
        self.valuerange = valuerange
        self._value = min(valuerange)
        super().__init__(*args, **kwargs)

    def _check_value(self, value):
        assert value in self.valuerange


class Spinbox(__Ranged, _base.Spinbox, Child):
    """A box for selecting a number with arrow buttons up and down."""

    can_focus = True


class Slider(_Oriented, __Ranged, _base.Slider, Child):
    """A slider for selecting a number."""
