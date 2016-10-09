"""Handy classes for BananaGUI."""

import collections
import functools
from gettext import gettext as _
import operator
import re

try:
    from collections.abc import Mapping
    from types import SimpleNamespace as NamespaceBase  # noqa
except ImportError:
    # In Python 3.3, the abstract base classes in collections were moved
    # to collections.abc and types.SimpleNamespace was addded.
    from collections import Mapping
    from argparse import Namespace as NamespaceBase  # noqa


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


class Font:
    """An immutable font type.

    >>> Font().bold = True
    Traceback (most recent call last):
      ...
    AttributeError: can't set attribute

    Usually it's a bad idea to use hard-coded fonts in your projects. If
    you want to customize the fonts it's recommended to allow your users
    to choose the fonts they want to use with a font dialog.
    """

    # Try to make the fonts immutable.
    __slots__ = ('_family', '_size', '_bold', '_italic', '_underline')
    family = property(operator.attrgetter('_family'),
                      doc="The font's family as a string or None.")
    size = property(operator.attrgetter('_size'),
                    doc="The font's size as an integer or None.")
    bold = property(operator.attrgetter('_bold'),
                    doc="True if the font is in bold.")
    italic = property(operator.attrgetter('_italic'),
                      doc="True if the font is italic.")
    underline = property(operator.attrgetter('_underline'),
                         doc="True if the font is underlined.")

    def __init__(self, family: str = None, size: int = None, *,
                 bold: bool = False, italic: bool = False,
                 underline: bool = False):
        """Create a new font.

        If family or size is None their default values will be used. If
        the family is 'monospace' (case-insensitive), a monospace font
        will be used even if a font with the name monospace is not
        available.

        >>> Font(' mONoSpACe   ')
        <BananaGUI font, family='monospace' size=None>
        >>> Font('Sans')
        <BananaGUI font, family='Sans' size=None>
        """
        if family is not None:
            assert family, "family cannot be empty"
            if family.lower().strip() == 'monospace':
                family = 'monospace'
        if size is not None:
            assert size > 0, "non-positive size %r" % (size,)
        self._family = family
        self._size = size
        self._bold = bold
        self._italic = italic
        self._underline = underline

    def __repr__(self):
        words = ['family=%r' % self.family, 'size=%r' % self.size]
        for attribute in ('bold', 'italic', 'underline'):
            value = getattr(self, attribute)
            if value:
                words.append('%s=%r' % (attribute, value))
        return '<BananaGUI font, %s>' % ' '.join(words)

    def __eq__(self, other):
        """Implement self == other using to_string().

        >>> Font('Sans', 16, bold=True) == Font('Sans', 16, bold=True)
        True
        >>> Font('Sans', 16, bold=True) == Font('Sans', 16)
        False
        >>> Font() == "Hello"
        False
        """
        if not isinstance(other, Font):
            return NotImplemented
        return self.to_string() == other.to_string()

    def __ne__(self, other):
        """Implement self != other using to_string().

        >>> Font('Sans', 16, bold=True) != Font('Sans', 16, bold=True)
        False
        >>> Font('Sans', 16, bold=True) != Font('Sans', 16)
        True
        >>> Font() != "Hello"
        True
        """
        if not isinstance(other, Font):
            return NotImplemented
        return self.to_string() != other.to_string()

    @classmethod
    def from_string(cls, string: str):
        """Parse a font from a string and return it.

        >>> Font.from_string('Sans, 16, bold italic')
        <BananaGUI font, family='Sans' size=16 bold=True italic=True>
        >>> Font.from_string(' Sans ,16,bOlD ItALic ')
        <BananaGUI font, family='Sans' size=16 bold=True italic=True>
        >>> Font.from_string('Sans, 16')
        <BananaGUI font, family='Sans' size=16>
        >>> Font.from_string('default family, 16')
        <BananaGUI font, family=None size=16>
        >>> Font.from_string('default family, default size')
        <BananaGUI font, family=None size=None>
        """
        try:
            if string.count(',') == 2:
                family, size, attributes = map(str.strip, string.split(','))
            elif string.count(',') == 1:
                family, size = map(str.strip, string.split(','))
                attributes = ''
            else:
                raise ValueError("the string should contain one or two commas")

            kwargs = dict.fromkeys(attributes.lower().split(), True)
            if family.lower() != 'default family':
                kwargs['family'] = family
            if size.lower() != 'default size':
                kwargs['size'] = int(size)
            return cls(**kwargs)

        except (AttributeError, IndexError, TypeError, ValueError) as e:
            raise ValueError("invalid font string %r" % (string,)) from e

    def _to_string(self, translations):
        def translate(string):
            return translations.get(string, string)

        result = []
        if self.family is None:
            result.append(translate("default family"))
        else:
            result.append(self.family)
        if self.size is None:
            result.append(translate("default size"))
        else:
            result.append(str(self.size))
        attributes = [translate(attribute)
                      for attribute in ('bold', 'italic', 'underline')
                      if getattr(self, attribute)]
        if attributes:
            result.append(' '.join(attributes))
        return ', '.join(result)

    def to_string(self):
        """Convert the font to a string.

        The strings can be parsed by Font.from_string, and they are
        readable enough for displaying them to the users of the program.

        >>> Font().to_string()
        'default family, default size'
        >>> Font(bold=True, underline=True).to_string()
        'default family, default size, bold underline'
        >>> Font('Sans', 123, italic=True).to_string()
        'Sans, 123, italic'
        """
        return self._to_string({})

    def to_translated_string(self):
        """Like to_string, but translates the string also.

        The translating is done with gettext.gettext. Use this for
        displaying fonts to the user. There is no from_translated_string.
        """
        return self._to_string({
            "default family": _("default family"),
            "default size": _("default size"),
            "bold": _("bold"),
            "italic": _("italic"),
            "underline": _("underline"),
        })


class Color(collections.namedtuple('Color', 'r g b')):
    """An immutable color.

    The colors are based on a namedtuple, so they behave a lot like
    (r, g, b) tuples. Actually they are (r, g, b) tuples.
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
    def from_hex(cls, hexstring: str):
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
        int16 = functools.partial(int, base=16)
        return cls(*map(int16, match.groups()))

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
    def from_rgbstring(cls, rgbstring: str):
        """Create a color from a CSS-compatible color string.

        This supports percents.

        >>> Color.from_rgbstring('rgb(255,100%,0)')
        Color(r=255, g=255, b=0)
        >>> Color.from_rgbstring('rG B ( 255 , 100% ,0) ')
        Color(r=255, g=255, b=0)
        """
        match = re.search(
            r'^rgb\((\d+%?),(\d+%?),(\d+%?)\)$',
            ''.join(rgbstring.split()),  # Remove whitespace.
            flags=re.IGNORECASE,
        )
        if match is None:
            raise ValueError("invalid RGB color string %r" % (rgbstring,))

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


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
