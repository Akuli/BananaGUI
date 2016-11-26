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

try:
    from collections import abc as abcoll
except ImportError:
    # Python 3.2, there's no separate collections.abc.
    import collections as abcoll

from bananagui import _base, utils
from .basewidgets import Parent, Child, Oriented


# This is not a Child because Window is based on this.
@utils.add_property('child')
class Bin(_base.Bin, Parent):
    """A widget that may contain one child widget.

    Attributes:
      child     The child in the widget.
                This can be None and this is None by default.
    """

    def __init__(self, *args, **kwargs):
        self._child = None
        super().__init__(*args, **kwargs)

    def _check_child(self, child):
        if child is not None:
            assert isinstance(child, Child)
            assert child.parent is self


class Box(abcoll.MutableSequence, Oriented, _base.Box, Parent, Child):
    """A widget that contains other widgets next to or above each other.

    To access the children just treat the Box object like a list:

        box.append(child)   # add a child
        box.remove(child)   # remove a child
        box[0]              # get the first child
        box[:3]             # get a list of first three children
        del box[:3]         # remove first three children
        box[:]              # get a list of children
        if box: ...         # check if there's children in the box
    """
    # The base should define an _append method that adds a child widget
    # to the end of the box and a _remove method that removes a child.

    def __init__(self, *args, **kwargs):
        self._children = []
        super().__init__(*args, **kwargs)

    def _set_children(self, new):
        assert len(new) == len(set(new)), "cannot add same child twice"
        old = self[:]

        # TODO: Maybe old and new have something else in common than the
        # beginning? Optimize this.
        common = utils.common_beginning(old, new)
        for child in old[common:]:
            self._remove(child)
        for child in new[common:]:
            assert isinstance(child, Child)
            assert child.parent is self
            self._append(child)

        self._children = new

    def __setitem__(self, item, value):
        children = self[:]
        children[item] = value
        self._set_children(children)

    def __getitem__(self, item):
        return self._children[item]

    def __delitem__(self, item):
        children = self[:]
        del children[item]
        self._set_children(children)

    def __len__(self):
        return len(self._children)

    # MutableMapping doesn't do this because it doesn't require that
    # subclasses support slicing. We also can't use functools.wraps()
    # to get the doc because then abc will think that our insert is
    # an abstract method that needs to be overrided.
    def insert(self, index, value):
        self[index:index] = [value]

    insert.__doc__ = abcoll.MutableSequence.insert.__doc__


# TODO: allow scrolling in one direction only.
class Scroller(_base.Scroller, Bin, Child):
    """A container that adds scrollbars around its child.

    The scroller displays a horizontal and a vertical scrollbar
    automatically when needed.
    """
