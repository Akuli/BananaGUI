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

from bananagui import Property, utils
from . import bases


class LayoutBase:
    pass


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
    children = Property('children', required_type=tuple, default=())

    def _bananagui_set_children(self, children):
        # This method is more complex than other methods in this class
        # because the children cannot be inserted in the middle, they
        # can only be prepended, appended or removed.

        assert len(children) == len(set(children)), \
            "cannot add the same child twice"

        def check(child):
            assert isinstance(child, bases.ChildBase), \
                "invalid child type %r" % type(child).__name__
            assert child['parent'] is self, \
                "cannot add a child with the wrong parent"

        common_beginning = utils.common_beginning(self, children)
        common_end = utils.common_beginning(reversed(self), reversed(children))

        if common_beginning + common_end == len(children):
            # Widgets are being removed from the middle and nothing else
            # is done.
            #
            #       do nothing       remove       do nothing
            # |--------------------|--------|--------------------|
            #    common_beginning                 common_end
            if common_end == 0:
                # Don't screw up with slicing.
                to_be_removed = self[common_beginning:]
            else:
                to_be_removed = self[common_beginning:-common_end]
            for child in to_be_removed:
                super().remove(child)

        # If this code runs, something is added to the middle of the box
        # and we need to remove other widgets temporarily to be able to
        # do that.
        elif common_beginning > common_end:
            # Many common items in the beginning, modify the end.
            #
            #                            add/remove    remove
            #         do nothing          children   temporarily
            # |-------------------------|----------|-------------|
            #       common_beginning                  common_end
            for child in self[common_beginning:]:
                super().remove(child)
            for child in children[common_beginning:]:
                check(child)
                super().append(child)
        else:
            # Many common items in the end, modify the beginning.
            # Python's lists aren't good at adding items to or removing
            # items from the beginning repeatedly, but lists aren't used
            # for that here.
            #
            #     remove     add/remove
            #   temporarily   children          do nothing
            # |-------------|----------|------------------------|
            # common_beginning                 common_end
            if common_end == 0:
                # We need to handle this specially because -0 == 0 and
                # slicing gets screwed up. Earlier common_beginning was
                # not bigger than common_end, so it is also 0. So
                # there's nothing in common, and we need to remove
                # everything and add everything again.
                for child in self:
                    super().remove(child)
                for child in children:
                    check(child)
                    super().prepend(child)
            else:
                for child in self[:-common_end]:
                    super().remove(child)
                for child in reversed(children[:-common_end]):
                    check(child)
                    super().prepend(child)

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
            return list(self['children'])[item]
        return super().__getitem__(item)

    def __delitem__(self, item):
        """Delete widget(s) from self and call super()."""
        if isinstance(item, (int, slice)):
            children = self[:]
            del children[item]
            self['children'] = tuple(children)
        else:
            super().__delitem__(item)

    # More list-like behavior. Some of these methods avoid indexing and
    # slicing self because that way there's no need to create a list in
    # __setitem__, __getitem__ or __delitem__

    def prepend(self, child):
        """Add a widget to the beginning of the box."""
        self['children'] = (child,) + self['children']

    def append(self, child):
        """Add a widget to the end of the box."""
        self['children'] += (child,)

    def remove(self, child):
        """Remove a widget from self."""
        children = self[:]
        children.remove(child)
        self[:] = children

    def __contains__(self, item):
        return item in self['children']

    def __len__(self):
        return len(self['children'])

    def __reversed__(self):
        return reversed(self['children'])

    def clear(self):
        """Remove all widgets from self."""
        self['children'] = ()

    def count(self, child):
        """Check how many times a child has been added.

        This is always 0 or 1 because children can only be added once.
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
        assert isinstance(index, int), "pop indices must be integers"
        result = self[index]
        del self[index]
        return result

    def reverse(self):
        """Reverse the box, making last items first and first items last.

        Note that unlike with lists, modifying the beginning of a box is
        usually more efficient than reversing the box, modifying the end
        of the box and reversing again.
        """
        self['children'] = self['children'][::-1]


class HBox:
    """A horizontal box."""

    _bananagui_bases = ('BoxBase',)
    _bananagui_orientation = 'h'  # Convinience attribute for wrappers.


class VBox:
    """A vertical box."""

    _bananagui_bases = ('BoxBase',)
    _bananagui_orientation = 'v'
