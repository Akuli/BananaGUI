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

"""Layout widgets."""

# TODO: Add a grid widget.

from bananagui import _base, Property, bananadoc
from bananagui.utils import baseclass, common_beginning, ListLikeBase
from .bases import _Oriented, Parent, Child


# This is not a Child because Window and Dialog are based on this.
@baseclass
@bananadoc
class Bin(_base.Bin, Parent):
    """A widget that contains one child widget or no children at all."""

    child = Property(
        'child', allow_none=True, default=None, type=Child,
        doc="""The child in the widget, None by default.

        Setting this to None removes the child.
        """)

    def _bananagui_set_child(self, child):
        if child is not None:
            assert child['parent'] is self, \
                "cannot add a child with the wrong parent"
        super()._bananagui_set_child(child)


class _BoxBase:
    """A base class for implementing Box's list-like behavior."""

    children = Property(
        'children', type=tuple, default=(),
        doc="A tuple of children in this widget.")
    _bananagui_contentproperty = 'children'

    def _bananagui_set_children(self, children):
        assert len(children) == len(set(children)), \
            "cannot add the same child twice"

        # TODO: Maybe self and children have something else in common
        # than the beginning? Optimize this.
        common = common_beginning(self, children)
        for child in self[common:]:
            # This assumes that super().remove and super().append
            # come from _base.Box.
            super().remove(child)
        for child in children[common:]:
            assert child['parent'] is self, \
                "cannot add a child with the wrong parent"
            super().append(child)


@bananadoc
class Box(_Oriented, ListLikeBase, _BoxBase, _base.Box, Parent, Child):
    """A widget that contains other widgets in a row.

    Boxes can be indexed and sliced like lists to modify their children,
    and slicing a box returns a list of children. Subscripting with a
    string still sets or gets the value of a property like for any other
    BananaGUI object. You can also set the value of the children
    property directly, it's a tuple of children.
    """
