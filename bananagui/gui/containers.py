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

import bananagui
from bananagui import _base, utils
from bananagui.structures import CallbackList  # Not imported in __init__.
from .basewidgets import Parent, Child, Oriented


# This is not a Child because Window is based on this.
@utils.baseclass
@bananagui.document_props
class Bin(_base.Bin, Parent):
    """A widget that contains one child widget or no children at all."""

    child = bananagui.BananaProperty(
        'child', allow_none=True, default=None, type=Child,
        doc="""The child in the widget, None by default.

        Setting this to None removes the child.
        """)

    def _bananagui_set_child(self, child):
        if child is not None:
            assert child['parent'] is self, \
                "cannot add a child with the wrong parent"
        super()._bananagui_set_child(child)


@bananagui.document_props
class Box(Oriented, _base.Box, Parent, Child):
    """A widget that contains other widgets.

    The children property behaves like a list and you can modify it to
    add widgets to the box or remove widgets from the box.
    """
    # The base should define a _bananagui_box_append method that adds a
    # child widget to the end of the box and a _bananagui_box_remove
    # method that removes a child widget from the box.

    children = bananagui.BananaProperty(
        'children', getdefault=CallbackList,
        doc="""A mutable sequence of children in the box.

        Setting this sets the sequence's content, the actual value never
        changes.
        """)

    def __init__(self, parent, **kwargs):
        self['children']._callbacks.append(self.__children_changed)
        super().__init__(parent, **kwargs)

    def _bananagui_set_children(self, children):
        """Set the content of the child list and return it."""
        self['children'][:] = children
        return self['children']

    def __children_changed(self, old, new):
        assert len(new) == len(set(new)), \
            "cannot add the same child twice"

        # TODO: Maybe old and new have something else in common than the
        # beginning? Optimize this.
        common = utils.common_beginning(old, new)
        for child in old[common:]:
            self._bananagui_box_remove(child)
        for child in new[common:]:
            assert isinstance(child, Child), \
                "expected a BananaGUI child widget, got %r" % (child,)
            assert child['parent'] is self, \
                "cannot add a child with the wrong parent"
            self._bananagui_box_append(child)


# TODO: allow scrolling in one direction only.
@bananagui.document_props
class Scroller(_base.Scroller, Bin, Child):
    """A container that adds scrollbars around its child.

    The scroller displays a horizontal and a vertical scrollbar
    automatically when needed.
    """
