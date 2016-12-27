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
from bananagui import types, utils
from .basewidgets import Child, _Oriented


def _valuecheck(widget, value):
    if value not in widget.valuerange:
        raise ValueError("value %r is out of %r"
                         % (value, widget.valuerange))


@types.add_property('value', extra_setter=_valuecheck, add_changed=True)
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

    def __init__(self, *args, value=None, **kwargs):
        if not isinstance(self.valuerange, range):
            raise TypeError("valuerange needs to be a range object, not %r"
                            % (self.valuerange,))
        if len(self.valuerange) < 2:
            raise ValueError("valuerange %r contains too little values"
                             % (self.valuerange,))
        # Ranges can't have a step of 0.
        if utils.rangestep(self.valuerange) < 0:
            raise ValueError("valuerange has negative step")
        super().__init__(*args, **kwargs)

    def _repr_parts(self):
        return [
            'value=' + repr(self.value),
            'valuerange=' + repr(self.valuerange),
        ] + super()._repr_parts()


class Spinbox(_Ranged, Child):
    """A widget for selecting an integer.

        ,-----------------------.
        | 123           | + | - |
        `-----------------------'

    Currently spinboxes can't be used with floats because the allowed
    values are represented by a Python range object, so you need to use
    an Entry if you want to use floats.
    """

    can_focus = True

    def __init__(self, valuerange, *, value=None, **kwargs):
        self.valuerange = valuerange
        self._value = min(valuerange)
        baseclass = bananagui._get_base('widgets.ranged:Spinbox')
        self._base = baseclass(self, valuerange)
        super().__init__(**kwargs)
        if value is not None:
            self.value = value


class Slider(_Oriented, _Ranged, Child):
    """A slider for selecting a number.

        |
        O   -----O--------
        |
        |
        |

    Currently floats aren't supported. If you want float support, let
    me know and I'll implement it.
    """

    def __init__(self, valuerange, *, orientation,
                 value=None, **kwargs):
        self.orientation = orientation
        self.valuerange = valuerange
        self._value = min(valuerange)
        baseclass = bananagui._get_base('widgets.ranged:Slider')
        self._base = baseclass(self, orientation, valuerange)
        super().__init__(**kwargs)
        if value is not None:
            self.value = value
