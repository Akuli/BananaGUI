# TODO: Add a grid widget.

import abc
import collections.abc
import functools

from bananagui import Orient, _modules
from .base import UpdatingProperty, Widget, ChildWidget, Parent


def _common_beginning(*iterables):
    """Check how many common elements the beginnings of iterables have.

    >>> common_beginning('abcd', 'abdc')
    2
    >>> common_beginning('abcd', 'bacd')
    0
    """
    result = 0
    for row in map(iter, zip(*iterables)):
        first = next(row)
        if not all(item == first for item in row):
            break
        result += 1

    return result


class Bin(Parent, metaclass=abc.ABCMeta):
    """Base class for widgets that may contain only one child at a time.

    See `Layout widgets`_ if you want to have multiple widgets in a Bin
    widget. This whole concept may seem stupid, but BananaGUI would be
    more complicated without separate Bin widgets and layout widgets.
    """

    def __init__(self, child=None, **kwargs):
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

    def children(self):
        return [] if self.child is None else [self.child]

    # Dialog has a custom gtk add
    _this_is_a_dialog = False

    def add(self, child):
        """Add a :class:`.ChildWidget` into this widget.

        This widget must not contain another child. The :attr:`~child`
        attribute will be set to the new child.
        """
        if self.child is not None:
            raise ValueError("there's already a child widget, remove "
                             "it before adding another widget")
        self._prepare_add(child)
        self.__child = child

        child.render(self)
        child.update_everything()

        if _modules.name == 'tkinter':
            # FIXME: implement expandiness properly, see comments in base.py
            #fills = {(False, False): 'none', (True, True): 'both',
            #         (True, False): 'x', (False, True): 'y'}
            #child.real_widget.pack(fill=fills[child.expand], expand=True)
            child.real_widget.pack(fill='both', expand=True)
        elif _modules.name in ['gtk2', 'gtk3']:
            child.real_widget.show()
            if not self._this_is_a_dialog:
                # Dialog does its own stuff instead of this
                self.real_widget.add(child.real_widget)
        else:   # pragma: no cover
            raise NotImplementedError

    def remove(self, child):
        """Remove the child from the widget.

        The :attr:`~child` attribute is set to None. The argument must
        be the old value of :attr:`~child`.
        """
        self._prepare_remove(child)   # makes sure that child is self.child
        self.__child = None

        if _modules.name == 'tkinter':
            child.real_widget.pack_forget()
        elif _modules.name.startswith('gtk'):
            if not self._this_is_a_dialog:
                self.real_widget.remove(child.real_widget)
        else:   # pragma: no cover
            raise NotImplementedError


#class Box(collections.abc.MutableSequence, Parent, Child):
#    """A widget that contains other widgets next to or above each other.
#
#    .. code-block:: none
#
#       ,----------.
#       |  box[0]  |    ,-----------------------------------.
#       |----------|    |   box[0]  |   box[1]  |   box[2]  |
#       |  box[1]  |    `-----------------------------------'
#       |----------|
#       |  box[2]  |
#       `----------'
#
#    To access the children just treat the Box object like a list::
#
#       box.append(child)   # add a child
#       box.remove(child)   # remove a child
#       box[0]              # get the first child
#       box[:3]             # get a list of first three children
#       del box[:3]         # remove first three children
#       box[:]              # get a list of children
#       if box: ...         # check if there are children in the box
#
#    Unfortunately ``random.shuffle(box)`` doesn't work because it wants
#    to temporarily add the same children to the box twice. You need to
#    do this instead::
#
#       children = box[:]
#       random.shuffle(children)
#       box[:] = children
#
#    .. seealso:: The :class:`.Checkbox` widget has nothing to do with
#                 this widget, but it has a similar name so you might be
#                 looking for it.
#    """
#    # The wrapper should define append and remove methods.
#
#    def __init__(self, orient=Orient.VERTICAL, **kwargs):
#        """Initialize the Box."""
#        self.__orient = Orient(orient)
#        self.__children = []
#        wrapperclass = _get_wrapper('widgets.parents:Box')
#        self._wrapper = wrapperclass(self, self.__orient)
#        super().__init__(**kwargs)
#
#    @property
#    def orient(self):
#        """The orient set on initialization.
#
#        This is always a :class:`bananagui.Orient` member.
#        """
#        return self.__orient
#
#    @functools.wraps(Parent.children)
#    def children(self):
#        yield from self
#
#    def _repr_parts(self):
#        parts = super()._repr_parts()
#        if self.orient == Orient.HORIZONTAL:
#            # Not the default.
#            parts.insert(0, 'horizontal')
#        return parts
#
#    def __set_children(self, new):
#        # TODO: Maybe the old and new children have something else in
#        # common than the beginning? Optimize this.
#        common = _common_beginning(self.__children, new)
#        for child in self.__children[common:]:
#            self._prepare_remove(child)
#            self._wrapper.remove(child._wrapper)
#        del self.__children[common:]
#        for child in new[common:]:
#            self._prepare_add(child)
#            self._wrapper.append(child._wrapper)
#            self.__children.append(child)
#
#    def __setitem__(self, item, value):
#        children = self[:]
#        children[item] = value
#        self.__set_children(children)
#
#    def __getitem__(self, item):
#        return self.__children[item]
#
#    def __delitem__(self, item):
#        children = self[:]
#        del children[item]
#        self.__set_children(children)
#
#    def __len__(self):
#        return len(self.__children)
#
#    # MutableSequence doesn't do this because it doesn't require that
#    # subclasses support slicing. We also can't use functools.wraps() to
#    # get the doc because then abc will think that our insert is an
#    # abstract method that needs to be overrided.
#    def insert(self, index, value):
#        """Insert an item to the box at the index."""
#        self[index:index] = [value]
#
#
## TODO: allow scrolling in one direction only and add tkinter support.
#class Scroller(Bin, Child):
#    """A widget that adds scrollbars around its child.
#
#    .. code-block:: none
#
#       ,-------------.
#       |           | |
#       |           | |
#       |    big    | |
#       |   child   | |
#       |   widget  | |
#       |           |o|
#       |           |o|
#       |           |o|
#       |___________|_|
#       |  ooo        |
#       `-------------'
#
#    The scroller displays a horizontal and a vertical scrollbar
#    automatically when needed.
#
#    .. note:: This widget is currently not available on Tkinter.
#    """
#
#    def __init__(self, child=None, **kwargs):
#        """Initialize the scroller."""
#        wrapperclass = _get_wrapper('widgets.parents:Scroller')
#        self._wrapper = wrapperclass(self)
#        super().__init__(child, **kwargs)
#
#
#@types.add_property('text', type=str, doc="The text at the top of the group.")
#class Group(Bin, Child):
#    """A widget for grouping other related widgets together.
#
#    .. code-block:: none
#
#       ,- Group -----------.
#       |                   |
#       |                   |
#       |    child widget   |
#       |                   |
#       |                   |
#       `-------------------'
#    """
#
#    def __init__(self, text='', child=None, **kwargs):
#        """Initialize the Group widget."""
#        wrapperclass = _get_wrapper('widgets.parents:Group')
#        self._wrapper = wrapperclass(self)
#        self._prop_text = ''
#        super().__init__(child, **kwargs)
#        self.text = text
#
#    def _repr_parts(self):
#        return ['text=%r' % self._prop_text] + super()._repr_parts()
#
