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

# TODO: Add a grid widget.

import collections.abc
import functools

from bananagui import _get_wrapper, Orient, types, utils
from .basewidgets import Child, Widget


# This and Bin aren't based on Child because Window is based on Bin.
class Parent(Widget):
    """A base class for widgets that contain other widgets."""

    def children(self):
        """Return an iterator of this widget's children.

        Dictionaries have a ``keys()`` method that returns a set-like
        view of the keys. This method is similar, but this returns an
        iterator instead of a view and the iterator yields
        :class:`.Child` widgets instead of keys.

        Subclasses of :class:`~Parent` provide different kinds of ways to
        access the children, but all Parent widgets have a children
        method that works consistently.
        """
        raise NotImplementedError("children() wasn't overrided")

    def _prepare_add(self, child):
        """Make sure child can be added to self and make it ready for it."""
        if child in self.children():
            raise ValueError("cannot add the same child twice")
        if child._parent is None:
            child._parent = self
        elif child._parent is not self:
            raise RuntimeError(
                "the child widget has already been in another widget, "
                "it can't be added to this widget anymore. See "
                "help('bananagui.widgets.Child').")

    def _prepare_remove(self, child):
        """Make sure that a child can be removed from self."""
        if child not in self.children():
            raise ValueError("cannot remove %r, hasn't been added" % (child,))

    def _repr_parts(self):
        parts = super()._repr_parts()

        length = 0
        for child in self.children():
            length += 1

        if length == 0:
            parts.append('empty')
        elif length == 1:
            parts.append('contains a child')
        else:
            parts.append('contains %d children' % length)
        return parts


class Bin(Parent):
    """Base class for widgets that may contain only one child at a time.

    See `Layout widgets`_ if you want to have multiple widgets in a Bin
    widget. This whole concept may seem stupid, but BananaGUI would be
    more complicated without separate Bin widgets and layout widgets.
    """

    def __init__(self, child=None, **kwargs):
        """Initialize the widget and add the child if it's given."""
        self.__child = None
        super().__init__(**kwargs)
        if child is not None:
            self.add(child)

    @property
    def child(self):
        """The child in the widget.

        This can be None and this is None by default. Use :meth:`~add`
        and :meth:`remove` or an initialization argument to set this.
        """
        return self.__child

    @functools.wraps(Parent.children)
    def children(self):
        if self.__child is not None:
            yield self.__child

    def add(self, child: Child):
        """Add a child widget into this widget.

        This widget must not contain another child. The :attr:`~child`
        attribute will be set to the new child.
        """
        if self.child is not None:
            raise ValueError("there's already a child, cannot add()")
        self._prepare_add(child)
        self._wrapper.add(child._wrapper)
        self.__child = child

    def remove(self, child: Child):
        """Remove the child from the widget.

        The child attribute is set to None. The argument must be the
        Child widget that is currently in this widget.
        """
        self._prepare_remove(child)
        # Now we are sure that child is self.__child.
        self.__child = None
        self._wrapper.remove(child._wrapper)
        # child._parent is left as is here.


class Box(collections.abc.MutableSequence, Parent, Child):
    """A widget that contains other widgets next to or above each other.

    .. code-block:: none

       ,----------.
       |  box[0]  |    ,-----------------------------------.
       |----------|    |   box[0]  |   box[1]  |   box[2]  |
       |  box[1]  |    `-----------------------------------'
       |----------|
       |  box[2]  |
       `----------'

    To access the children just treat the Box object like a list::

       box.append(child)   # add a child
       box.remove(child)   # remove a child
       box[0]              # get the first child
       box[:3]             # get a list of first three children
       del box[:3]         # remove first three children
       box[:]              # get a list of children
       if box: ...         # check if there are children in the box

    Unfortunately ``random.shuffle(box)`` doesn't work because it wants
    to temporarily add the same children to the box twice. You need to
    do this instead::

       children = box[:]
       random.shuffle(children)
       box[:] = children

    .. seealso:: The :class:`.Checkbox` widget has nothing to do with
                 this widget, but it has a similar name so you might be
                 looking for it.
    """
    # The wrapper should define append and remove methods.

    def __init__(self, orient=Orient.VERTICAL, **kwargs):
        """Initialize the Box."""
        self.__orient = Orient(orient)
        self.__children = []
        wrapperclass = _get_wrapper('widgets.parents:Box')
        self._wrapper = wrapperclass(self, self.__orient)
        super().__init__(**kwargs)

    @property
    def orient(self):
        """The orient set on initialization.

        This is always a :class:`bananagui.Orient` member.
        """
        return self.__orient

    @functools.wraps(Parent.children)
    def children(self):
        yield from self

    def _repr_parts(self):
        parts = super()._repr_parts()
        if self.orient == Orient.HORIZONTAL:
            # Not the default.
            parts.insert(0, 'horizontal')
        return parts

    def __set_children(self, new):
        # TODO: Maybe the old and new children have something else in
        # common than the beginning? Optimize this.
        common = utils.common_beginning(self.__children, new)
        for child in self.__children[common:]:
            self._prepare_remove(child)
            self._wrapper.remove(child._wrapper)
        del self.__children[common:]
        for child in new[common:]:
            self._prepare_add(child)
            self._wrapper.append(child._wrapper)
            self.__children.append(child)

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

    # MutableSequence doesn't do this because it doesn't require that
    # subclasses support slicing. We also can't use functools.wraps() to
    # get the doc because then abc will think that our insert is an
    # abstract method that needs to be overrided.
    def insert(self, index, value):
        """Insert an item to the box at the index."""
        self[index:index] = [value]


# TODO: allow scrolling in one direction only and add tkinter support.
class Scroller(Bin, Child):
    """A widget that adds scrollbars around its child.

    .. code-block:: none

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

    .. note:: This widget is currently not available on Tkinter.
    """

    def __init__(self, child=None, **kwargs):
        """Initialize the scroller."""
        wrapperclass = _get_wrapper('widgets.parents:Scroller')
        self._wrapper = wrapperclass(self)
        super().__init__(child, **kwargs)


@types.add_property('text', type=str, doc="The text at the top of the group.")
class Group(Bin, Child):
    """A widget for grouping other related widgets together.

    .. code-block:: none

       ,- Group -----------.
       |                   |
       |                   |
       |    child widget   |
       |                   |
       |                   |
       `-------------------'
    """

    def __init__(self, text='', child=None, **kwargs):
        """Initialize the Group widget."""
        wrapperclass = _get_wrapper('widgets.parents:Group')
        self._wrapper = wrapperclass(self)
        self._prop_text = ''
        super().__init__(child, **kwargs)
        self.text = text

    def _repr_parts(self):
        return ['text=%r' % self._prop_text] + super()._repr_parts()
