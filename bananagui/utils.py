"""BananaGUI's utility functions and other things."""

import importlib


def all_equal(iterable):
    """Return True if all elements of iterable are equal.

    iterable must contain at least one element.

    >>> all_equal([1, 1.0])
    True
    >>> all_equal([1, 2])
    False
    """
    iterator = iter(iterable)
    first = next(iterator)
    for element in iterator:
        if element != first:
            return False
    return True


def common_beginning(*iterables):
    """Check how many common elements the beginnings of iterables have.

    >>> common_beginning([1, 2, 3, 4], [1, 2, 4, 3])
    2
    >>> common_beginning([2, 1, 3, 4], [1, 2, 3, 4])
    0
    """
    assert len(iterables) >= 2
    result = 0
    rows = iter(zip(*iterables))
    try:
        while all_equal(next(rows)):
            result += 1
    except StopIteration:
        pass
    return result


def global_members(modulename):
    """A decorator that exposes Enum members as global variables."""
    module = importlib.import_module(modulename)

    def inner(the_enum):
        # Iterating over the enum doesn't include aliases.
        for name, member in the_enum.__members__.items():
            setattr(module, name, member)
        return the_enum

    return inner
