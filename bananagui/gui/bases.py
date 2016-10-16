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

"""Base classes for various widgets."""

from bananagui import (
    _base, bananadoc, Color, Property, BananaObject,
    HORIZONTAL, VERTICAL)
from bananagui.utils import baseclass


@baseclass
@bananadoc
class Widget(_base.Widget, BananaObject):
    """A widget baseclass."""

    # The tooltip property is not implemented here. Parent widgets don't
    # need tooltips because they should be always filled with Dummy
    # widgets.
    real_widget = Property(
        'real_widget', settable=False,
        doc="The real GUI toolkit's widget that BananaGUI uses.")
    background = Property(
        'background', type=Color, allow_none=True, default=None,
        doc="""The widget's background.

        The system-specific default is used if this is None.
        """)


@baseclass
@bananadoc
class Parent(_base.Parent, Widget):
    """A widget that child widgets can use as their parent."""


@baseclass
@bananadoc
class Child(_base.Child, Widget):
    """A widget that can be added to a container.

    Children take a parent argument on initialization. The parent
    property can be used to retrieve it, but the parent cannot be
    changed afterwards.
    """

    parent = Property('parent', type=Parent, settable=False,
                      doc="The parent set on initialization.")
    tooltip = Property(
        'tooltip', type=str, allow_none=True, default=None,
        doc="""Text in the widget's tooltip.

        This is None if the widget doesn't have a tooltip.
        """)
    expand = Property(
        'expand', how_many=2, type=bool, default=(True, True),
        doc="""Two-tuple of horizontal and vertical expanding.

        For example, (True, True) will make the widget expand in
        both directions.

        **Note:** When multiple widgets are next to each other in a
        container, at least one of them needs to expand in the
        container's direction. Like this:

            ,------------------------------------------------.
            |   non-   |                                     |
            |expanding |           expanding widget          |
            |  widget  |                                     |
            `------------------------------------------------'

        Not like this:

            ,------------------------------------------------.
            |   non-   |   non-   |                          |
            |expanding |expanding |       empty space        |
            |  widget  |  widget  |                          |
            `------------------------------------------------'

        This way the children will behave consistently with all GUI
        toolkits. You can use a Dummy widget to fill the empty
        space:

            ,------------------------------------------------.
            |   non-   |   non-   |                          |
            |expanding |expanding |       Dummy widget       |
            |  widget  |  widget  |                          |
            `------------------------------------------------'

        """)
    grayed_out = Property(
        'grayed_out', type=bool, default=False,
        doc="True if the widget is grayed out, False otherwise.")

    def __init__(self, parent: Parent, **kwargs):
        self.parent.raw_set(parent)
        super().__init__(**kwargs)


@baseclass
@bananadoc
class Oriented:
    """Implement an orientation property and handy class methods.

    There are many ways to create instances of _Oriented widgets. For
    example, all of these are valid ways to create a horizontal widget:

        SomeWidget.horizontal(...)
        SomeWidget(..., orientation='h')
        SomeWidget(..., orientation=bananagui.HORIZONTAL)
    """

    orientation = Property(
        'orientation', settable=False,
        doc="""This is bananagui.HORIZONTAL or bananagui.VERTICAL.

        This is set with the last positional argument on initialization
        and cannot be changed afterwards.
        """)

    def __init__(self, *args, orientation, **kwargs):
        assert orientation in {HORIZONTAL, VERTICAL}, \
            "unknown orientation %r" % (orientation,)
        self.orientation.raw_set(orientation)
        super().__init__(*args, **kwargs)

    @classmethod
    def horizontal(cls, *args, **kwargs):
        """Create and return a new horizontal instance."""
        return cls(*args, orientation=HORIZONTAL, **kwargs)

    @classmethod
    def vertical(cls, *args, **kwargs):
        """Create and return a new vertical instance"""
        return cls(*args, orientation=VERTICAL, **kwargs)


@baseclass
@bananadoc
class Ranged:
    """Implement minimum, maximum, step and value BananaGUI properties.

    Unlike with Python's range, the minimum and maximum are inclusive.
    """
    minimum = Property(
        'minimum', type=int, settable=False,
        doc="The smallest possible value set on initialization.")
    maximum = Property(
        'maximum', type=int, settable=False,
        doc="The largest possible value set on initialization.")
    step = Property(
        'step', type=int, settable=False,
        doc="How much the value will be incremented/decremented at a time.")
    value = Property('value', type=int,
                     doc="The current value.")

    def __init__(self, *args, minimum: int = 0, maximum: int = 100,
                 step: int = 1, **kwargs):
        """Set the minimum, maximum and step properties."""
        assert minimum < maximum, "minimum must be smaller than maximum"
        assert step > 0, "non-positive step %d" % step
        assert maximum - minimum >= step, "too big step"
        self.minimum.raw_set(minimum)
        self.maximum.raw_set(maximum)
        self.step.raw_set(step)
        self.value.raw_set(minimum)

        # This makes checking values easier.
        self._bananagui_ranged_valuerange = range(minimum, maximum+1, step)
        super().__init__(*args, **kwargs)

    def _bananagui_set_value(self, value):
        assert value in self._bananagui_ranged_valuerange, \
            "value %s is out of range" % value
        super()._bananagui_set_value(value)
