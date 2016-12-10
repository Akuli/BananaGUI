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


@utils.add_property('value', add_changed=True)
class _Ranged:
    """Implement valuerange and value BananaGUI properties.

    Attributes:
      valuerange        The value range set on initialization.
      value             The widget's current value.
                        This needs to be in valuerange and it's the
                        smallest value of valuerange by default.
      on_value_changed  List of callbacks that are ran when value changes.
    """
    # Subclasses should get a valuerange argument on initialization,
    # set the valuerange attribute to it and set the _value attribute
    # to min() of that range.

    def __init__(self, *args, **kwargs):
        assert isinstance(self.valuerange, range)
        assert len(self.valuerange) >= 2
        assert utils.rangestep(self.valuerange) > 0
        super().__init__(*args, **kwargs)

    def _check_value(self, value):
        assert value in self.valuerange


class Spinbox(_Ranged, Child):
    """A box for selecting a number with arrow buttons up and down."""

    can_focus = True

    def __init__(self, parent, *, valuerange, **kwargs):
        self.valuerange = valuerange
        self._value = min(valuerange)
        baseclass = bananagui._get_base('widgets.ranged:Spinbox')
        self.base = baseclass(self, parent, valuerange)
        super().__init__(parent, **kwargs)


class Slider(_Oriented, _Ranged, Child):
    """A slider for selecting a number."""

    def __init__(self, parent, *, orientation, valuerange, **kwargs):
        self.orientation = orientation
        self.valuerange = valuerange
        self._value = min(valuerange)
        baseclass = bananagui._get_base('widgets.ranged:Slider')
        self.base = baseclass(self, parent, orientation, valuerange)
        super().__init__(parent, **kwargs)
