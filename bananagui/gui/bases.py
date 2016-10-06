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

from bananagui import _base
from bananagui.types import Property, BananaObject, bananadoc
from bananagui.utils import baseclass


@baseclass
@bananadoc
class Widget(_base.Widget, BananaObject):
    """A widget baseclass."""

    real_widget = Property(
        'real_widget',
        doc="The real GUI toolkit's widget that BananaGUI uses.")


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

    Properties:

        expand          RW
            Two-tuple of horizontal and vertical expanding.
    """

    parent = Property('parent', type=Parent,
                      doc="The parent set on initialization.")
    expand = Property(
        'expand', pair=True, type=bool, default=(True, True), settable=True,
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
        'grayed_out', type=bool, default=False, settable=True,
        doc="True if the widget is grayed out, False otherwise.")
    tooltip = Property(
        'tooltip', type=str, allow_none=True, default=None, settable=True,
        doc="""Text in the widget's tooltip.

        This is None if the widget doesn't have a tooltip.
        """)

    def __init__(self, parent: Parent):
        super().__init__()
        self.parent.raw_set(parent)


@bananadoc
class Dummy(_base.Dummy, Child):
    """An empty widget."""
