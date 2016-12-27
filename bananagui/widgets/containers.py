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
    import collections.abc as abcoll
except ImportError:
    # Python 3.2, there's no separate collections.abc.
    import collections as abcoll

import bananagui
from bananagui import utils
from .basewidgets import Parent, Child, _Oriented


_wrong_parent_msg = (
    "the child widget has already been in another widget, "
    "it can't be added to this widget anymore. See "
    "help('bananagui.widgets.Child').")


# This is not a Child because Window is based on this.
class Bin(Parent):
    """A widget that may contain one child widget.

    Attributes:
      child     The child in the widget.
                This can be None and this is None by default.
    """

    # It's impossible to give a child on initialization because this
    # widget needs to exist before a child can be created into this.
    def __init__(self, child=None):
        self.__child = None
        super().__init__()
        if child is not None:
            self.add(child)

    @property
    def child(self):
        return self.__child

    def _repr_parts(self):
        if self.__child is None:
            part = "contains nothing"
        else:
            part = "contains a child"
        return super()._repr_parts() + [part]

    def add(self, child):
        if self.__child is not None:
            raise RuntimeError("there's already a child, cannot add()")
        if not isinstance(child, Child):
            raise TypeError("expected a Child widget, got %r" % (child,))
        if child._parent is None:
            child._parent = self
        elif child._parent is not self:
            raise RuntimeError(_wrong_parent_msg)
        self._base.add(child._base)
        self.__child = child

    def remove(self, child):
        if child is None:
            raise ValueError("cannot remove None")
        if child is not self.__child:
            raise ValueError("cannot remove a child that is not in "
                             "the widget")
        self._base.remove(child._base)
        # child._parent is left as is here.


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

    Unfortunately random.shuffle(box) doesn't work because it wants to
    temporarily add the same children to the box twice. You need to do
    this instead:

        children = box[:]
        random.shuffle(children)
        box[:] = children
    """
    # The base should define append and remove methods.

    def __init__(self, *, orientation, **kwargs):
        self.__children = []
        baseclass = bananagui._get_base('widgets.containers:Box')
        self._base = baseclass(self, orientation)
        self.orientation = orientation
        super().__init__(**kwargs)

    def _repr_parts(self):
        end = "one child" if len(self) == 1 else "%d children" % len(self)
        return super()._repr_parts() + ["contains " + end]

    def __set_children(self, new):
        assert len(new) == len(set(new)), "cannot add same child twice"
        old = self[:]

        # TODO: Maybe old and new have something else in common than the
        # beginning? Optimize this.
        common = utils.common_beginning(old, new)
        for child in old[common:]:
            self._base.remove(child._base)
        for child in new[common:]:
            assert isinstance(child, Child)
            if child._parent is None:
                child._parent = self
            elif child._parent is not self:
                raise RuntimeError(_wrong_parent_msg)
            self._base.append(child._base)

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
        """Insert an item to the box, before the index."""
        self[index:index] = [value]


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

    def __init__(self, *args, **kwargs):
        baseclass = bananagui._get_base('widgets.containers:Scroller')
        self._base = baseclass(self)
        super().__init__(*args, **kwargs)
