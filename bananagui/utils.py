"""blah blah blah

It's not recommended to rely on this submodule. It's meant only for
being used internally by BananaGUI and it can be changed in the future.
"""

# TODO: fix the docstring


try:
    from types import SimpleNamespace as NamespaceBase  # noqa
except ImportError:
    # types.SimpleNamespace are new in Python 3.3.
    from argparse import Namespace as NamespaceBase  # noqa


def check(value, *, allow_none=False, required_type=None, length=None,
          minimum=None, maximum=None):
    if value is None:
        assert allow_none, "the value must not be None"
        return
    if required_type is not None:
        assert isinstance(value, required_type), \
            ("expected an instance of %s, got %r"
             % (required_type.__name__, value))
    if length is not None:
        assert len(value) == length, \
            "expected a value of length %d, got %r" % (length, value)
    if minimum is not None:
        assert value >= minimum, "%r is smaller than %r" % (value, minimum,)
    if maximum is not None:
        assert value <= maximum, "%r is larger than %r" % (value, maximum,)


def check_integer_pair(pair):
    """Make sure that two items of a pair are positive integers."""
    check(pair, required_type=tuple, length=2)
    first, second = pair
    assert isinstance(first, int), "expected an integer, got %r" % (pair,)
    assert isinstance(second, int), "expected an integer, got %r" % (pair,)


def check_positive_integer_pair(pair):
    """Make sure that two items of a pair are positive integers."""
    check_integer_pair(pair)
    first, second = pair
    assert first > 0, "expected a value bigger than 0, got %r" % (first,)
    assert second > 0, "expected a value bigger than 0, got %r" % (second,)


# TODO: remove this and its usage
def check_size(size):
    import warnings
    warnings.warn("use check_positive_integer_pair, not check_size",
                  DeprecationWarning)
    check_positive_integer_pair(size)


def check_bool_pair(pair):
    check(pair, required_type=tuple, length=2)
    first, second = pair
    assert isinstance(first, bool), "%r is not a Boolean" % (first,)
    assert isinstance(second, bool), "%r is not a Boolean" % (second,)


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
