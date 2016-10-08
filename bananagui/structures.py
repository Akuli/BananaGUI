"""Handy classes for BananaGUI."""

import functools

try:
    from collections.abc import Mapping
    from types import SimpleNamespace as NamespaceBase  # noqa
except ImportError:
    # In Python 3.3, the abstract base classes in collections were moved
    # to collections.abc and types.SimpleNamespace was addded.
    from argparse import Namespace as NamespaceBase  # noqa
    from collections import Mapping


@Mapping.register
class FrozenDict:
    """An immutable-ish dictionary-like object.

    >>> d = FrozenDict(a=1, b=2, c=3)   # arguments like for dict()
    >>> d == {'a': 1, 'b': 2, 'c': 3}   # comparing to dicts
    True
    >>> d == FrozenDict(a=1, b=2, c=3)  # comparing to FrozenDicts
    True
    >>> from collections.abc import Mapping
    >>> isinstance(d, Mapping)  # they are mappings
    True
    >>> isinstance(d, dict)     # but not regular dicts
    False
    >>> {d: 123}         # can be used as dict keys  # doctest: +ELLIPSIS
    {FrozenDict(...): 123}
    """

    # Try to make this immutable.
    __slots__ = ('_data',)

    def __init__(self, *args, **kwargs):
        """Initialize the new FrozenDict.

        All arguments are treated like for a regular dictionary.
        """
        self._data = dict(*args, **kwargs)

    @functools.wraps(dict.__repr__)
    def __repr__(self):
        return 'FrozenDict(%r)' % (self._data,)

    @functools.wraps(dict.__contains__)
    def __contains__(self, item):
        return item in self._data

    @functools.wraps(dict.__getitem__)
    def __getitem__(self, item):
        return self._data[item]

    @functools.wraps(dict.__iter__)
    def __iter__(self):
        return iter(self._data)

    @functools.wraps(dict.__len__)
    def __len__(self):
        return len(self._data)

    @classmethod
    @functools.wraps(dict.fromkeys)
    def fromkeys(cls, iterable, value=None):
        return cls(dict.fromkeys(iterable, value))

    @functools.wraps(dict.get)
    def get(self, key, default=None):
        return self._data.get(key, default)

    @functools.wraps(dict.items)
    def items(self):
        return self._data.items()

    @functools.wraps(dict.keys)
    def keys(self):
        return self._data.keys()

    @functools.wraps(dict.values)
    def values(self):
        return self._data.values()

    # We can't wrap this because dict.__hash__ is None.
    def __hash__(self):
        """Return a hash of items in the dictionary."""
        # Dictionaries don't rely entirely on hashes of their keys, so
        # they can have FrozenDict({'a': 1}) and frozenset({('a', 1)})
        # as two different keys.
        return hash(frozenset(self.items()))

    @functools.wraps(dict.__eq__)
    def __eq__(self, other):
        # This will make two FrozenDicts compare their _data.
        #
        #                  self.__eq__(other)
        #                           |
        #                           |
        #                  self._data == other
        #                /                     \
        #               /                       \
        #    self._data.__eq__(other)   other.__eq__(self._data)
        #              |                          |
        #              |            ,---------------------------.
        #       NotImplemented      | other._data == self._data |
        #                           `---------------------------'
        return self._data == other

    @functools.wraps(dict.__ne__)
    def __ne__(self, other):
        return self._data != other


class Callback:
    """Much like functools.partial.

    The difference is that the initializatoin arguments are added to the
    end instead of the beginning. This also doesn't allow keyword
    arguments when calling.

    >>> c = Callback(print, "World!", sep='-')
    >>> c
    Callback(<built-in function print>, 'World!', sep='-')
    >>> # Typically BananaGUI would call this internally with something
    >>> # like an event as an argument.
    >>> c("Hello")
    Hello-World!
    """

    def __init__(self, function, *extra_args, **extra_kwargs):
        """Initialize the callback."""
        assert callable(function), "%r is not callable" % (function,)
        self._function = function
        self._extra_args = extra_args
        self._extra_kwargs = extra_kwargs

    def __call__(self, *beginning_args):
        """Call the function."""
        all_args = beginning_args + self._extra_args
        return self._function(*all_args, **self._extra_kwargs)

    def __repr__(self):
        """Return a nice string representation of the callback."""
        words = [repr(self._function)]
        words.extend(map(repr, self._extra_args))
        words.extend('%s=%r' % item for item in self._extra_kwargs.items())
        return 'Callback(%s)' % ', '.join(words)


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
