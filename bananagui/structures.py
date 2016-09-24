"""Handy classes for BananaGUI."""

import functools

try:
    from collections.abc import Mapping
except ImportError:
    # The abstract base classes in collections were moved to
    # collections.abc in Python 3.3.
    from collections import Mapping


@Mapping.register
class FrozenDict:
    """An immutable-ish dictionary-like object."""

    __slots__ = ('_dict',)

    def __init__(self, *args, **kwargs):
        """Initialize the new FrozenDict.

        Positional and keyword arguments are treated like for a regular
        dictionary.
        """
        self._dict = dict(*args, **kwargs)

    @functools.wraps(dict.__repr__)
    def __repr__(self):
        # printf-formatting can actually handle dictionaries just fine
        # even without wrapping the dictionary in a tuple or another
        # dictionary of length one.
        return 'FrozenDict(%r)' % self._dict

    @functools.wraps(dict.__contains__)
    def __contains__(self, item):
        return item in self._dict

    @functools.wraps(dict.__getitem__)
    def __getitem__(self, item):
        return self._dict[item]

    @functools.wraps(dict.__iter__)
    def __iter__(self):
        return iter(self._dict)

    @functools.wraps(dict.__len__)
    def __len__(self):
        return len(self._dict)

    @classmethod
    @functools.wraps(dict.fromkeys)
    def fromkeys(cls, iterable, value=None):
        return cls(dict.fromkeys(iterable, value))

    @functools.wraps(dict.get)
    def get(self, key, default=None):
        return self._dict.get(key, default)

    @functools.wraps(dict.items)
    def items(self):
        return self._dict.items()

    @functools.wraps(dict.keys)
    def keys(self):
        return self._dict.keys()

    @functools.wraps(dict.values)
    def values(self):
        return self._dict.values()

    @functools.wraps(dict.__eq__)
    def __eq__(self, other):
        if isinstance(other, Mapping):
            # This will make two FrozenDicts compare their _dicts.
            #
            #                  self.__eq__(other)
            #                           |
            #                           |
            #                  self._dict == other
            #                /                     \
            #               /                       \
            #    self._dict.__eq__(other)   other.__eq__(self._dict)
            #              |                          |
            #              |            ,---------------------------.
            #       NotImplemented      | other._dict == self._dict |
            #                           `---------------------------'
            return self._dict == other
        return NotImplemented

    @functools.wraps(dict.__ne__)
    def __ne__(self, other):
        if isinstance(other, Mapping):
            return self._dict != other
        return NotImplemented
