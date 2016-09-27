"""BananaGUI's utility functions and other things.

It's not recommended to rely on this submodule. It's meant only for
being used internally by BananaGUI and it can be changed in the future.
"""

# TODO: fix the docstring

try:
    from types import SimpleNamespace as NamespaceBase  # noqa
except ImportError:
    # types.SimpleNamespace are new in Python 3.3.
    from argparse import Namespace as NamespaceBase  # noqa


def copy_doc(source):
    """Copy __doc__ to another object.

    Unlike functools.wraps, this only copies __doc__ so this also works
    with classes. Use this as a context manager.
    """
    def inner(destination):
        destination.__doc__ = source.__doc__
        return destination

    return inner


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


class ClassProperty:
    """Like @property, but for classes.

    Unfortunately these don't support setters and deleters.
    """

    def __init__(self, getter):
        """Initialize the class property."""
        self._getter = getter

    def __get__(self, instance, cls):
        """Return the value."""
        return self._getter(cls)
