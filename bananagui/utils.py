"""BananaGUI's utility functions and other things.

It's not recommended to rely on this submodule. It's meant only for
being used internally by BananaGUI and it can be changed in the future.
"""

import re

# Other BananaGUI modules are free to use collections.abc from here.
try:
    from collections import abc    # noqa
except ImportError:
    # The abstract base classes in collections were moved from _abcoll
    # to collections.abc in Python 3.3.
    import _abcoll as abc   # noqa


# Allow None as a non-default value.
_NOTHING = object()


def baseclass(base):
    """Modify a class to prevent creating instances and return it.

    Subclasses of the class can be instantiated normally, and the class
    may define an __init__ method. Use this as a decorator.
    """
    def new_new(cls, *args, **kwargs):
        if cls is base:   # issubclass() can't be used here
            raise TypeError("cannot create instances of %r directly"
                            % cls.__name__)
        if old_new is object.__new__:
            # object.__new__ takes no arguments.
            return old_new(cls)
        return old_new(cls, *args, **kwargs)

    old_new = base.__new__
    base.__new__ = new_new
    return base


def common_beginning(*iterables):
    """Check how many common elements the beginnings of iterables have.

    >>> common_beginning([1, 2, 3, 4], [1, 2, 4, 3])
    2
    >>> common_beginning([2, 1, 3, 4], [1, 2, 3, 4])
    0
    """
    assert len(iterables) >= 2, "two items are needed for comparing"
    result = 0
    rows = iter(zip(*iterables))
    try:
        while len(set(next(rows))) == 1:  # All items of the row are equal.
            result += 1
    except StopIteration:
        pass
    return result


def check(value, *, how_many=1, allow_none=False, type=None,
          length=None, minimum=None, maximum=None):
    """Do assertions about the value."""
    if how_many != 1:
        # Everything is different.
        assert isinstance(value, tuple), "%r is not a tuple" % (value,)
        assert len(value) == how_many, \
            "length of %r is not %d" % (value, how_many)
        for element in value:
            check(element, allow_none=allow_none, type=type,
                  length=length, minimum=minimum, maximum=maximum)
        return

    if not allow_none:
        assert value is not None, "the value must not be None"
    if value is None:
        return
    if type is not None:
        assert isinstance(value, type), \
            "expected an instance of %r, got %r" % (type.__name__, value)
    if length is not None:
        assert len(value) == length, \
            "expected a value of length %d, got %r" % (length, value)
    if minimum is not None:
        assert value >= minimum, "%r is smaller than %r" % (value, minimum)
    if maximum is not None:
        assert value <= maximum, "%r is larger than %r" % (value, maximum)


def find_attribute(attribute, *objects):
    """Get an attribute from any of objects."""
    for obj in objects:
        try:
            return getattr(obj, attribute)
        except AttributeError:
            pass
    raise AttributeError("none of the objects have an attribute %r"
                         % attribute)


def register(abstract_baseclass):
    """Return a decorator that calls abstract_baseclass.register.

    @abstract_baseclass.register also works since Python 3.3, but this
    works on 3.2 also.
    """
    def inner(subclass):
        abstract_baseclass.register(subclass)
        return subclass

    return inner


def rangestep(range_object: range):
    """Return a range object's step.

    Unlike range_object.step, this also works on Python 3.2.
    """
    try:
        return range_object.step
    except AttributeError:
        if len(range_object) >= 2:
            # The range has enough items for calculating the step.
            return range_object[1] - range_object[0]
        # This hacky code only runs on Python 3.2.
        if repr(range_object).count(',') == 1:
            # The repr doesn't show the step, so it's the default.
            return 1
        # The repr shows the step so we can get it from that.
        match = re.search(r'(-?\d+)\)$', repr(range_object))
        return int(match.group(1))


@register(abc.MutableSequence)
class ListLikeBase:
    """A base class that implements list-like methods.

    A property called self._bananagui_contentproperty will be set to a
    tuple of the new content when the content is changed and it will be
    used to get the current content.
    """
    # TODO: example in docstring.

    def __repr__(self):
        return '<%s, %s=%r>' % (
            super().__repr__().lstrip('<').rstrip('>'),
            self._bananagui_contentproperty,
            self[:],
        )

    def __set(self, content):
        self[self._bananagui_contentproperty] = content

    def __get(self):
        return self[self._bananagui_contentproperty]

    def __setitem__(self, item, value):
        """Behave like a list if item's type allows that or call super."""
        if isinstance(item, (int, slice)):
            content = self[:]
            content[item] = value
            self.__set(tuple(content))
        else:
            super().__setitem__(item, value)

    def __getitem__(self, item):
        """Behave like a list if item's type allows that or call super."""
        if isinstance(item, int):
            return self.__get()[item]
        if isinstance(item, slice):
            return list(self.__get()[item])
        return super().__getitem__(item)

    def __delitem__(self, item):
        """Behave like a list if item's type allows that or call super."""
        if isinstance(item, (int, slice)):
            items = self[:]
            del items[item]
            self[:] = items
        else:
            super().__delitem__(item)

    def __contains__(self, item):
        """Check if item is in self."""
        return item in self.__get()

    def __len__(self):
        """Return the number of items in self."""
        return len(self.__get())

    def __reversed__(self):
        """Iterate the content of self reversed."""
        return reversed(self.__get())

    def append(self, item):
        """Add an item to end of self."""
        self.__set(self.__get() + (item,))

    def clear(self):
        """Remove all items from self."""
        del self[:]

    def count(self, item):
        """Check how many times an item has been added."""
        return self.__get().count(item)

    def extend(self, new_items):
        """Append each item in new_items to self."""
        # The built-in list.extend allows extending by anything
        # iterable, so this allows it also.
        self.__set(self.__get() + tuple(new_items))

    def index(self, item):
        """Return the index of item in self."""
        return self.__get().index(item)

    def insert(self, index, item):
        """Insert an item at the given index."""
        self[index:index] = [item]

    def pop(self, index: int = -1):
        """Delete self[index] and return the removed item.

        The index must be an integer.
        """
        result = self[index]
        del self[index]
        return result

    def remove(self, item):
        """Remove an item from self."""
        content = self[:]
        content.remove(item)
        self[:] = content

    def reverse(self):
        """Reverse self, making last items first and first items last."""
        self[:] = reversed(self)

    def sort(self, **kwargs):
        """Sort self."""
        self[:] = sorted(self, **kwargs)
