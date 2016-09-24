"""Handy classes for BananaGUI."""

try:
    from collections.abc import Mapping
except ImportError:
    # collections.abc is new in Python 3.3.
    from collections import Mapping


@Mapping.register
class FrozenDict:
    """An immutable-ish dictionary-like object."""

    __slots__ = ('_dict',)

    def __init__(self, *args, **kwargs):
        self._dict = dict(*args, **kwargs)

    def __repr__(self):
        # printf-formatting can actually handle dictionaries just fine
        # even without wrapping the dictionary in a tuple or another
        # dictionary of length one.
        return 'FrozenDict(%r)' % self._dict

    @classmethod
    def fromkeys(cls, iterable, value=None):
        return cls(dict.fromkeys(iterable, value))

    def __contains__(self, item):
        return item in self._dict

    def __getitem__(self, item):
        return self._dict[item]

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def get(self, key, default=None):
        return self._dict.get(key, default)

    def items(self):
        return self._dict.items()

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

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

    def __ne__(self, other):
        if isinstance(other, Mapping):
            return self._dict != other
        return NotImplemented
