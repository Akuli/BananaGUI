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

import bananagui
from bananagui import utils
from .basewidgets import Parent, Child, _Oriented


# This is not a Child because Window is based on this.
@utils.add_property('child')
class Bin(Parent):
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


class Box(abcoll.MutableSequence, _Oriented, Parent, Child):
    """A widget that contains other widgets next to or above each other.

        ,----------.
        |  box[0]  |    ,-----------------------------------.
        |----------|    |   box[0]  |   box[1]  |   box[2]  |
        |  box[1]  |    `-----------------------------------'
        |----------|
        |  box[2]  |
        `----------'

    To access the children just treat the Box object like a list:

        box.append(child)   # add a child
        box.remove(child)   # remove a child
        box[0]              # get the first child
        box[:3]             # get a list of first three children
        del box[:3]         # remove first three children
        box[:]              # get a list of children
        if box: ...         # check if there are children in the box
    """
    # The base should define append and remove methods.

    def __init__(self, parent, *, orientation, **kwargs):
        self.__children = []
        baseclass = bananagui._get_base('widgets.containers:Box')
        self.base = baseclass(self, parent, orientation)
        self.orientation = orientation
        super().__init__(parent, **kwargs)

    def __repr__(self):
        cls = type(self)
        if len(self) == 1:
            childcount = '1 child'
        else:
            childcount = '%d children' % len(self)
        return '<%s.%s object, contains %s>' % (
            cls.__module__, cls.__name__, childcount)

    def __set_children(self, new):
        assert len(new) == len(set(new)), "cannot add same child twice"
        old = self[:]

        # TODO: Maybe old and new have something else in common than the
        # beginning? Optimize this.
        common = utils.common_beginning(old, new)
        for child in old[common:]:
            self.base.remove(child)
        for child in new[common:]:
            assert isinstance(child, Child)
            assert child.parent is self, \
                "cannot add %r into %r" % (child, self)
            self.base.append(child)

        self.__children = new

    def __setitem__(self, item, value):
        children = self[:]
        children[item] = value
        self.__set_children(children)

    def __getitem__(self, item):
        return self.__children[item]

    def __delitem__(self, item):
        children = self[:]
        del children[item]
        self.__set_children(children)

    def __len__(self):
        return len(self.__children)

    # MutableMapping doesn't do this because it doesn't require that
    # subclasses support slicing. We also can't use functools.wraps()
    # to get the doc because then abc will think that our insert is
    # an abstract method that needs to be overrided.
    def insert(self, index, value):
        self[index:index] = [value]

    insert.__doc__ = abcoll.MutableSequence.insert.__doc__


# TODO: allow scrolling in one direction only.
class Scroller(Bin, Child):
    """A container that adds scrollbars around its child.

        ,-------------.
        |           | |
        |           | |
        |    big    | |
        |   child   | |
        |   widget  | |
        |           |o|
        |           |o|
        |           |o|
        |___________|_|
        |  ooo        |
        `-------------'

    The scroller displays a horizontal and a vertical scrollbar
    automatically when needed.
    """

    def __init__(self, parent, **kwargs):
        baseclass = bananagui._get_base('widgets.containers:Scroller')
        self.base = baseclass(self, parent)
        super().__init__(parent, **kwargs)
