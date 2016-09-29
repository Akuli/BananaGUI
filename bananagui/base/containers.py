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

#from bananagui import types, utils
import bananagui
from bananagui import utils, Property, check
from . import bases


@utils.baseclass
class ContainerBase:
    """A widget that child widgets can use as their parent."""

    _bananagui_bases = ('WidgetBase',)


@utils.baseclass
class BinBase:
    """A widget that contains one child widget or no children at all.

    Properties:
        child           RW
            The child in the widget, None by default. Setting this to
            None removes the child.
    """

    _bananagui_bases = ('ParentBase',)
    child = Property('child', allow_none=True, default=None)

    def _bananagui_set_child(self, child):
        # This isinstance check works because the loaded ChildBase
        # inherits from the ChildBase in this module.
        assert isinstance(child, ChildBase)
        assert child is None or child['parent'] is self
        super()._bananagui_set_child(child)


@utils.baseclass
class BoxBase:
    """A widget that contains other widgets in a row.

    Boxes can be indexed and sliced like lists to modify their children,
    and slicing a box returns a list of children. Subscripting with a
    string still sets or gets the value of a property like for any other
    BananaGUI object.

    Properties:
        children        RC
            A tuple of children in this widget.
            At least one of these widgets should always be expanding in
            the box's direction, for example, horizontally if the box is
            a HBox. Otherwise the result is unspecified.
    """

    _bananagui_bases = ('ParentBase', 'ChildBase')
    children = bananagui.Property('children', required_type=tuple, default=())

    def _bananagui_set_children(self, children):
        assert len(children) == len(set(children)), \
            "cannot add the same child twice"

        common_beginning = utils.common_beginning(self, children)

        # TODO: Maybe self and children have something else in common
        # than the beginning? Optimize this.
        for child in self[common_beginning:]:
            super().remove(child)
        for child in children[common_beginning:]:
            assert isinstance(child, bases.ChildBase), "invalid child type"
            assert child['parent'] is self
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


class HBox:
    """A horizontal box."""

    _bananagui_bases = ('BoxBase',)
    _bananagui_orientation = 'h'  # Convinience attribute for wrappers.


class VBox:
    """A vertical box."""

    _bananagui_bases = ('BoxBase',)
    _bananagui_orientation = 'v'
