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

from bananagui import _base
from bananagui.types import Property, bananadoc
from bananagui.utils import baseclass, common_beginning
from .bases import Parent, Child


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


@baseclass
@bananadoc
class Box(_base.Box, Parent, Child):
    """A widget that contains other widgets in a row.

    Boxes can be indexed and sliced like lists to modify their children,
    and slicing a box returns a list of children. Subscripting with a
    string still sets or gets the value of a property like for any other
    BananaGUI object. You can also set the value of the children
    property directly, it's a tuple of children.
    """

    children = Property(
        'children', type=tuple, default=(),
        doc="A tuple of children in this widget.")

    def _bananagui_set_children(self, children):
        assert len(children) == len(set(children)), \
            "cannot add the same child twice"

        common = common_beginning(self, children)

        # TODO: Maybe self and children have something else in common
        # than the beginning? Optimize this.
        for child in self[common:]:
            super().remove(child)
        for child in children[common:]:
            assert child['parent'] is self, \
                "cannot add a child with the wrong parent"
            super().append(child)

    def __setitem__(self, item, value):
        """Set widget(s) to self or call super()."""
        if isinstance(item, (int, slice)):
            children = self[:]
            children[item] = value
            self['children'] = tuple(children)
        else:
            super().__setitem__(item, value)

    def __getitem__(self, item):
        """Get widget(s) from self or call super()."""
        if isinstance(item, int):
            return self['children'][item]
        if isinstance(item, slice):
            return list(self['children'][item])
        return super().__getitem__(item)

    def __delitem__(self, item):
        """Delete widget(s) from self or call super()."""
        if isinstance(item, (int, slice)):
            children = self[:]
            del children[item]
            self[:] = children
        else:
            super().__delitem__(item)

    # More list-like behavior. Some of these methods avoid indexing and
    # slicing self because that way there's no need to create a list in
    # __setitem__, __getitem__ or __delitem__

    def __contains__(self, item):
        """Check if item is a child in the box."""
        return item in self['children']

    def __len__(self):
        """Return the number of children in the box."""
        return len(self['children'])

    def __reversed__(self):
        """Iterate the children of the box in reverse."""
        return reversed(self['children'])

    def append(self, child):
        """Add a widget to the box."""
        self['children'] += (child,)

    def clear(self):
        """Remove all widgets from self."""
        self[:] = []

    def count(self, child):
        """Check how many times a child has been added.

        This always returns 0 or 1 because children can be added once
        only. This method is provided just for compatibility with lists
        and using `child in self` instead is recommended.
        """
        result = self['children'].count(child)
        assert result in (0, 1)
        return result

    def extend(self, new_children):
        """Append each child in new_children to self."""
        # The built-in list.extend() allows extending by anything
        # iterable, so this allows it also.
        self['children'] += tuple(new_children)

    def index(self, child):
        """Return the index of child in self."""
        return self['children'].index(child)

    def insert(self, index, child):
        """Insert a child at the given index."""
        # This doesn't break if index is negative.
        self[index:index] = [child]

    def pop(self, index=-1):
        """Delete self[index] and return the removed item.

        The index must be an integer.
        """
        assert isinstance(index, int)
        result = self[index]
        del self[index]
        return result

    def remove(self, child):
        """Remove a widget from self."""
        children = self[:]
        children.remove(child)
        self[:] = children

    def reverse(self):
        """Reverse the box, making last items first and first items last.

        Unlike with lists, this isn't very efficient.
        """
        self[:] = self[::-1]

    def sort(self, **kwargs):
        """Sort self."""
        self[:] = sorted(self, **kwargs)


@bananadoc
class HBox(_base.HBox, Box):
    """A horizontal box."""


@bananadoc
class VBox(_base.VBox, Box):
    """A vertical box."""
