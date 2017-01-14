# Copyright (c) 2016-2017 Akuli

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

"""Parent subclasses."""
# TODO: Add a grid widget.

import abc
try:
    import collections.abc as abcoll
except ImportError:
    # Python 3.2, there's no separate collections.abc.
    import collections as abcoll

import bananagui
from bananagui import types, utils
from .basewidgets import Child, Widget


# This and Bin aren't based on Child because Window is based on Bin.
class Parent(Widget, metaclass=abc.ABCMeta):
    """A base class for widgets that contain other widgets."""

    def _prepare_add(self, child):
        """Make sure child can be added to self and make it ready for it."""
        if not isinstance(child, Child):
            raise TypeError("expected a Child widget, got %r" % (child,))
        if child._parent is None:
            child._parent = self
        elif child._parent is not self:
            raise RuntimeError(
                "the child widget has already been in another widget, "
                "it can't be added to this widget anymore. See "
                "help('bananagui.widgets.Child').")

    def iter_children(self, *, recursive=False):
        """Yield all children of this Parent widget.

        If recursive is True, also yield all of the childrens'
        children. This is consistent and works the same way with
        different kinds of Parent widgets.
        """
        # Subclasses should provide _get_children().
        for child in self._get_children():
            yield child
            if recursive and isinstance(child, Parent):
                # yield from is new in Python 3.3.
                for subchild in child.iter_children(recursive=True):
                    yield subchild

    @abc.abstractmethod
    def _get_children(self):
        """Return an iterable of all child widgets this widget has."""

    def _repr_parts(self):
        parts = super()._repr_parts()
        childcount = 0
        for child in self.iter_children():
            childcount += 1
        if childcount == 0:
            parts.append('empty')
        elif childcount == 1:
            parts.append('contains a child')
        else:
            parts.append('contains %d children' % childcount)
        return parts


class Bin(Parent):
    """A widget that may contain one child widget."""

    def __init__(self, child=None, **kwargs):
        self.__child = None
        super().__init__(**kwargs)
        if child is not None:
            self.add(child)

    @property
    def child(self):
        """The child in the widget.

        This can be None and this is None by default. Use add() and
        remove() or an initialization argument to set this.
        """
        return self.__child

    def _get_children(self):
        if self.child is not None:
            yield self.child

    def add(self, child):
        """Add the child widget into this widget.

        This widget must not contain another child. The value of the
        child property will be set to the new child.
        """
        if self.child is not None:
            raise RuntimeError("there's already a child, cannot add()")
        self._prepare_add(child)
        self._wrapper.add(child._wrapper)
        self.__child = child

    def remove(self, child):
        """Remove the child from the widget

        The child attribute is set to None. The argument must be a
        Child widget that is currently in this widget.
        """
        if child is None:
            raise ValueError("cannot remove None")
        if child is not self.__child:
            raise ValueError("cannot remove a child that is not in "
                             "the widget")
        self.__child = None
        self._wrapper.remove(child._wrapper)
        # child._parent is left as is here.


class Box(abcoll.MutableSequence, Parent, Child):
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
    # The wrapper should define append and remove methods.

    def __init__(self, orient=bananagui.VERTICAL, **kwargs):
        """Initialize the Box."""
        self.__orient = bananagui.Orient(orient)
        self.__children = []
        wrapperclass = bananagui._get_wrapper('widgets.parents:Box')
        self._wrapper = wrapperclass(self, self.__orient)
        super().__init__(**kwargs)

    @property
    def orient(self):
        """The orient set on initialization.

        This is always a bananagui.Orient member.
        """
        return self.__orient

    def _repr_parts(self):
        parts = super()._repr_parts()
        if self.orient == bananagui.HORIZONTAL:
            # Not the default.
            parts.append('orient=bananagui.HORIZONTAL')
        return parts

    def _get_children(self):
        return self     # self is iterable.

    def __set_children(self, new):
        if len(new) != len(set(new)):
            raise ValueError("cannot add same child twice")
        old = self[:]

        # TODO: Maybe old and new have something else in common than the
        #       beginning? Optimize this.
        common = utils.common_beginning(old, new)
        for child in old[common:]:
            self._wrapper.remove(child._wrapper)
        for child in new[common:]:
            self._prepare_add(child)
            self._wrapper.append(child._wrapper)
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

    def __init__(self, child=None, **kwargs):
        wrapperclass = bananagui._get_wrapper('widgets.parents:Scroller')
        self._wrapper = wrapperclass(self)
        super().__init__(child, **kwargs)


@types.add_property('text', type=str,
                    doc="The text at the top of the group.")
class Group(Bin, Child):
    """A widget for grouping other related widgets together.

    ,- Group -----------.
    |                   |
    |                   |
    |    child widget   |
    |                   |
    |                   |
    `-------------------'
    """

    def __init__(self, text='', child=None, **kwargs):
        wrapperclass = bananagui._get_wrapper('widgets.parents:Group')
        self._wrapper = wrapperclass(self)
        self._text = ''
        super().__init__(child, **kwargs)
        self.text = text

    def _repr_parts(self):
        return ['text=%r' % self.text] + super()._repr_parts()
