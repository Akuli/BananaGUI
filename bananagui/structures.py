"""Handy classes for BananaGUI."""

import collections
import functools
import re

try:
    from collections.abc import Mapping
except ImportError:
    # The abstract base classes in collections were moved to
    # collections.abc in Python 3.3.
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
    >>> isinstance(d, dict)   # but they aren't instances of built-in dict
    False
    >>> {d: 123}              # can be used as dict keys  # doctest: +ELLIPSIS
    {...: 123}
    """

    __slots__ = ('_data',)

    def __init__(self, *args, **kwargs):
        """Initialize the new FrozenDict.

        All arguments are treated like for a regular dictionary.
        """
        self._data = dict(*args, **kwargs)

    @functools.wraps(dict.__repr__)
    def __repr__(self):
        # printf-formatting can actually handle dictionaries just fine
        # even without wrapping the dictionary in a tuple or another
        # dictionary of length one.
        return 'FrozenDict(%r)' % self._data

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
        # as their keys.
        return hash(frozenset(self.items()))

    @functools.wraps(dict.__eq__)
    def __eq__(self, other):
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
        return self._data == other

    @functools.wraps(dict.__ne__)
    def __ne__(self, other):
        return self._data != other


class Font(collections.namedtuple(
        'Font', 'family size bold italic underline')):
    """A font.

    Fonts are based on a namedtuple, so they behave much like other
    namedtuples.

    >>> Font().bold = True
    Traceback (most recent call last):
      ...
    AttributeError: can't set attribute
    >>> Font('Sans', 16, bold=True) == Font('Sans', 16, bold=True)
    True
    >>> Font('Sans', 16, bold=True) == Font('Sans', 16)
    False
    >>> list(Font())  # [family, size, bold, italic, underline]
    [None, None, False, False, False]

    Fonts can also be stored in strings using from_string() and
    to_string().

    Usually it's a bad idea to use hard-coded fonts in your projects. If
    you want to customize the fonts it's recommended to allow your users
    to choose the fonts they want to use.
    """

    def __new__(cls, family=None, size=None, *, bold=False,
                italic=False, underline=False):
        """Create a new font.

        If family or size is None their default values will be used. If
        the family is 'monospace' (case-insensitive), a monospace font
        will be used even if a font with the name monospace is not
        available.

        >>> Font('mONoSpACe')             # doctest: +ELLIPSIS
        Font(family='monospace', ...)
        >>> Font('Sans')                  # doctest: +ELLIPSIS
        Font(family='Sans', ...)
        """
        if family is not None:
            if not isinstance(family, str):
                raise TypeError("expected None or a string, got %r"
                                % (family,))
            if not family:
                raise ValueError("family cannot be an empty string")
            if family.lower() == 'monospace':
                family = 'monospace'

        if size is not None:
            if not isinstance(size, int):
                raise TypeError("expected None or an integer, got %r"
                                % (size,))
            if size <= 0:
                raise ValueError("%d is not a valid font size" % size)

        for value in (bold, italic, underline):
            if not isinstance(value, bool):
                raise TypeError("expected a Boolean, got %r" % (value,))

        return super().__new__(cls, family, size, bold, italic, underline)

    @classmethod
    def from_string(cls, string):
        """Parse a font from a string and return it.

        >>> Font.from_string('Sans, 16, bold italic')   # doctest: +ELLIPSIS
        Font(family='Sans', size=16, bold=True, italic=True, ...)
        >>> Font.from_string(' Sans ,16,bOlD ItALic ')  # doctest: +ELLIPSIS
        Font(family='Sans', size=16, bold=True, italic=True, ...)
        >>> Font.from_string('Sans, 16')  # doctest: +ELLIPSIS
        Font(family='Sans', size=16, bold=False, italic=False, ...)
        >>> Font.from_string('default family, default size')
        Font(family=None, size=None, bold=False, italic=False, underline=False)
        """
        if not isinstance(string, str):
            raise TypeError("expected a string, got %r" % (string,))

        try:
            if string.count(',') == 2:
                family, size, attributes = string.split(',')
            elif string.count(',') == 1:
                family, size = string.split(',')
                attributes = ''
            else:
                raise ValueError("the string should contain one or two commas")

            kwargs = {}
            family = family.strip()
            if family.lower() != 'default family':
                kwargs['family'] = family
            size = size.strip()
            if size.lower() != 'default size':
                kwargs['size'] = int(size)
            kwargs.update(dict.fromkeys(attributes.lower().split(), True))

        except (AttributeError, IndexError, TypeError, ValueError) as e:
            raise ValueError("invalid font string %r" % string) from e

        return cls(**kwargs)

    def to_string(self):
        """Convert the font to a string.

        The strings can be parsed by Font.from_string, and they are
        readable enough for displaying them to the users of the program.

        >>> Font().to_string()
        'default family, default size'
        >>> Font(underline=True).to_string()
        'default family, default size, underline'
        >>> Font('Sans', 123, underline=True).to_string()
        'Sans, 123, underline'
        """
        # It's OK to rely on falsiness of None because family and size
        # are checked in __new__.
        result = [self.family or 'default family',
                  str(self.size or 'default size')]

        attributes = [attribute
                      for attribute in ('bold', 'italic', 'underline')
                      if getattr(self, attribute)]
        if attributes:
            result.append(' '.join(attributes))

        return ', '.join(result)


class Color(collections.namedtuple('Color', 'r g b')):
    """An immutable color.

    The colors are based on a namedtuple, so they behave a lot like
    (r, g, b) tuples.
    """

    def __init__(self, r, g, b):
        """Check the r, g and b values."""
        # Most of the initialization is done by the namedtuple's
        # __new__. See Color._source.
        for value in (r, g, b):
            assert value in range(256), "invalid r/g/b value %r" % (value,)

    @property
    def brightness(self):
        """Brightness of the color.

        >>> Color(0, 0, 0).brightness
        0.0
        >>> Color(255, 255, 255).brightness
        1.0
        >>> Color(51, 51, 51).brightness
        0.2
        """
        return sum(self) / 3 / 255

    @classmethod
    def from_hex(cls, hexstring):
        """Create a color from a hexadecimal color string.

        This also supports 4-character hexadecmial colors. For example,
        '#ff0' is treated as '#ffff00'.

        >>> Color.from_hex('#ffff00')
        Color(r=255, g=255, b=0)
        >>> Color.from_hex('#FfFF00')
        Color(r=255, g=255, b=0)
        >>> Color.from_hex('#ff0')
        Color(r=255, g=255, b=0)
        """
        if not isinstance(hexstring, str):
            raise TypeError("expected a string, got %r" % (hexstring,))
        if len(hexstring) == 4:
            # It's a 4-character hexadecimal color, like '#fff'.
            real_hexstring = hexstring[0]
            for character in hexstring[1:]:
                real_hexstring += character * 2
        else:
            real_hexstring = hexstring

        match = re.search('^#' + '([0-9a-f]{2})'*3 + '$',
                          real_hexstring, flags=re.IGNORECASE)
        if match is None:
            raise ValueError("invalid hexadecimal color string %r"
                             % (hexstring,))
        return cls(*(int(value, 16) for value in match.groups()))

    @property
    def hex(self):
        """Convert self to a hexadecimal color.

        >>> Color(1, 2, 3).hex
        '#010203'
        >>> Color(255, 255, 255).hex
        '#ffffff'
        """
        return '#%02x%02x%02x' % self

    @classmethod
    def from_rgbstring(cls, rgbstring):
        """Create a color from a CSS-compatible color string.

        This supports percents.

        >>> Color.from_rgbstring('rgb(255,100%,0)')
        Color(r=255, g=255, b=0)
        >>> Color.from_rgbstring('rGB ( 255 , 100% ,0) ')
        Color(r=255, g=255, b=0)
        """
        if not isinstance(rgbstring, str):
            raise TypeError("expected a string, got %r" % (rgbstring,))

        # Remove whitespace.
        rgbstring = ''.join(rgbstring.split())

        match = re.search(r'^rgb\((\d+%?),(\d+%?),(\d+%?)\)$', rgbstring,
                          flags=re.IGNORECASE)
        if match is None:
            raise ValueError("invalid RGB color string %r" % rgbstring)

        rgb = []
        for value in match.groups():
            if value.endswith('%'):
                rgb.append(int(value[:-1]) * 255 // 100)
            else:
                rgb.append(int(value))
        return cls(*rgb)

    @property
    def rgbstring(self):
        """Convert self to a CSS-compatible color string.

        >>> Color(255, 255, 0).rgbstring
        'rgb(255,255,0)'
        """
        return 'rgb(%d,%d,%d)' % self


class Callback:
    """Much like functools.partial.

    The difference is that the initializatoin arguments are added to the
    end instead of the beginning.

    >>> c = Callback(print, "World!")
    >>> # Typically BananaGUI would call this internally with something
    >>> # like an event as an argument.
    >>> c("Hello")
    Hello World!
    """

    def __init__(self, function, *extra_args):
        self._function = function
        self._extra_args = extra_args

    def __call__(self, *beginning_args):
        all_args = beginning_args + self._extra_args
        return self._function(*all_args)

    def __repr__(self):
        init_args = 
        arglist = ', '.join(map(repr, self._extra_args))
        return 'Callback(%s)' % arglist


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
