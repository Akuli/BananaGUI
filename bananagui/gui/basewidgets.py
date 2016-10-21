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

import bananagui
from bananagui import _base, utils


@utils.baseclass
@bananagui.bananadoc
class Widget(_base.Widget, bananagui.BananaObject):
    """A widget baseclass."""

    # The tooltip property is not implemented here. Parent widgets don't
    # need tooltips because they should be always filled with Dummy
    # widgets.
    real_widget = bananagui.Property(
        'real_widget', settable=False,
        doc="The real GUI toolkit's widget that BananaGUI uses.")


@utils.baseclass
@bananagui.bananadoc
class Parent(_base.Parent, Widget):
    """A widget that child widgets can use as their parent."""


@utils.baseclass
@bananagui.bananadoc
class Child(_base.Child, Widget):
    """A widget that can be added to a container.

    Children take a parent argument on initialization. The parent
    property can be used to retrieve it, but the parent cannot be
    changed afterwards.
    """

    parent = bananagui.Property('parent', type=Parent, settable=False,
                                doc="The parent set on initialization.")
    tooltip = bananagui.Property(
        'tooltip', type=str, allow_none=True, default=None,
        doc="""Text in the widget's tooltip.

        This is None if the widget doesn't have a tooltip.
        """)
    expand = bananagui.Property(
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
    grayed_out = bananagui.Property(
        'grayed_out', type=bool, default=False,
        doc="True if the widget is grayed out, False otherwise.")

    def __init__(self, parent: Parent, **kwargs):
        self.parent.raw_set(parent)
        super().__init__(**kwargs)


@utils.baseclass
@bananagui.bananadoc
class Oriented:
    """Implement an orientation property and handy class methods.

    There are many ways to create instances of Oriented subclasses. For
    example, all of these are valid ways to create a horizontal widget:

        SomeWidget.horizontal(...)
        SomeWidget(..., orientation='h')
        SomeWidget(..., orientation=bananagui.HORIZONTAL)
    """

    orientation = bananagui.Property(
        'orientation', settable=False,
        doc="""This is bananagui.HORIZONTAL or bananagui.VERTICAL.

        This is set with the last positional argument on initialization
        and cannot be changed afterwards.
        """)

    def __init__(self, *args, orientation, **kwargs):
        assert orientation in {bananagui.HORIZONTAL, bananagui.VERTICAL}, \
            "unknown orientation %r" % (orientation,)
        self.orientation.raw_set(orientation)
        super().__init__(*args, **kwargs)

    @classmethod
    def horizontal(cls, *args, **kwargs):
        """Create and return a new horizontal instance."""
        return cls(*args, orientation=bananagui.HORIZONTAL, **kwargs)

    @classmethod
    def vertical(cls, *args, **kwargs):
        """Create and return a new vertical instance"""
        return cls(*args, orientation=bananagui.VERTICAL, **kwargs)


def _check_valuerange(range_object):
    """Check if a range is valid for Ranged."""
    assert len(range_object) >= 2, \
        "%r contains less than two values" % (range_object,)
    assert utils.rangestep(range_object) > 0, \
        "%r has a non-positive step" % (range_object,)


@utils.baseclass
@bananagui.bananadoc
class Ranged:
    """Implement valuerange and value BananaGUI properties."""
    valuerange = bananagui.Property(
        'valuerange', type=range, settable=False,
        doc="""A range of allowed values.

        This must be a Python range object.
        """)
    value = bananagui.Property(
        'value', type=int,
        doc="""The current value.

        This must be in the valuerange.
        """)

    def __init__(self, *args, valuerange: range = range(11), **kwargs):
        """Set the value and range properties."""
        # The range is set before calling _check_valuerange because
        # setting it checks the type and we get better error messages.
        self.valuerange.raw_set(valuerange)
        _check_valuerange(valuerange)
        self.value.raw_set(min(valuerange))
        super().__init__(*args, **kwargs)

    def _bananagui_set_value(self, value):
        """Check if the value is in the range."""
        assert value in self['valuerange'], \
            "%r is not in %r" % (value, self['valuerange'])
        super()._bananagui_set_value(value)
