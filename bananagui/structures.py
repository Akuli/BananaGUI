"""Handy classes for BananaGUI."""

import collections
import functools
from gettext import gettext as _
import operator
import re
import sys

try:
    from collections import abc
    from types import SimpleNamespace as NamespaceBase  # noqa
except ImportError:
    # In Python 3.3, the abstract base classes in collections were moved
    # to collections.abc and types.SimpleNamespace was addded.
    import _abcoll as abc  # collections.py imports * from this.
    from argparse import Namespace as NamespaceBase  # noqa

from bananagui import utils


class _CallbackBase:
    """A mutable object that calls callbacks when it's mutated.

    The callbacks can be anything callable and they're stored in a
    _callbacks attribute. They will be called with the CallbackList as
    the only argument.
    """

    __slots__ = ('_data', '_callbacks')

    def __init__(self, *args, **kwargs):
        self._data = type(self)._basetype(*args, **kwargs)
        self._callbacks = []

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self._data)

    @classmethod
    def _expose(cls, name):
        """Add a function to cls that exposes a self._data method."""
        function = getattr(cls._basetype, name)

        @functools.wraps(function)
        def exposer(self, *args, **kwargs):
            # We can't use self._data.copy() because lists don't have a
            # copy method on Python 3.2.
            old_data = cls._basetype(self._data)
            result = function(self._data, *args, **kwargs)
            new_data = cls._basetype(self._data)

            if old_data != new_data:
                # It has been mutated.
                try:
                    for callback in self._callbacks:
                        callback(old_data, new_data)
                except Exception as e:
                    # A callback doesn't like the new data. Let's
                    # restore it back to what it was before and reraise
                    # the exception.
                    self._data = old_data
                    raise e

            return result

        setattr(cls, name, exposer)

    @classmethod
    def _expose_all(cls, *names):
        """Call self._expose with each name."""
        for name in names:
            cls._expose(name)


@utils.register(abc.MutableSequence)
class CallbackList(_CallbackBase):
    """A list that runs callbacks when its content changes.

    >>> def callback(old, new):
    ...     print("before cl contained", old, "and now it contains", new)
    ...
    >>> cl = CallbackList([1])
    >>> cl
    CallbackList([1])
    >>> cl[:]       # slicing and methods return regular lists
    [1]
    >>> cl._callbacks.append(callback)
    >>> cl.extend([2, 3, 4])
    before cl contained [1] and now it contains [1, 2, 3, 4]
    >>> cl[2:]      # again, a regular list
    [3, 4]
    >>> del cl[:]
    before cl contained [1, 2, 3, 4] and now it contains []
    >>> del cl[:]     # it was already empty, no need to run callbacks
    >>> cl
    CallbackList([])
    """

    __slots__ = ()  # Prevent attaching other attributes.
    _basetype = list


# The __eq__, __ne__, __gt__, __ge__, __lt__ and __le__ will make two
# CallbackLists compare each other's _data. For example, this is what
# __eq__ will do:
#
#                        a == b
#                           |
#                           |
#                      a.__eq__(b)
#                           |
#                           |
#                      a._data == b
#                    /              \
#                   /                \
#          a._data.__eq__(b)   b.__eq__(a._data)
#                 |                    |
#                 |          ,--------------------.
#           NotImplemented   | b._data == a._data |
#                            `--------------------'
CallbackList._expose_all(
    '__contains__', '__iter__',
    '__setitem__', '__getitem__', '__delitem__',
    '__eq__', '__ne__', '__gt__', '__ge__', '__lt__', '__le__',
    '__add__', '__mul__', '__iadd__', '__imul__',
    'append', 'count', 'extend', 'index', 'insert', 'pop',
    'remove', 'reverse', 'sort',
)
if sys.version_info >= (3, 3):
    CallbackList._expose_all('clear', 'copy')


@utils.register(abc.MutableMapping)
class CallbackDict(_CallbackBase):
    """A dictionary that runs callbacks when its content changes.

    >>> def callback(old, new):
    ...     print("before d contained", old, "and now it contains", new)
    ...
    >>> d = CallbackDict(a=1)
    >>> d
    CallbackDict({'a': 1})
    >>> d.copy()    # return a regular dictionary
    {'a': 1}
    >>> d._callbacks.append(callback)
    >>> del d['a']
    before d contained {'a': 1} and now it contains {}
    >>> d.update({'b': 2})
    before d contained {} and now it contains {'b': 2}
    >>> d['b'] = 2      # it was already 2, no need to run callbacks
    >>> d.clear()
    before d contained {'b': 2} and now it contains {}
    """

    __slots__ = ()
    _basetype = dict

    # We can't expose this like other methods because it's a
    # classmethod.
    @classmethod
    def fromkeys(cls, iterable, value=None):
        """Create a new CallbackDict from an iterable of keys.

        >>> CallbackDict.fromkeys(['lol'])
        CallbackDict({'lol': None})
        >>> CallbackDict.fromkeys(['lol'], 'wtf')
        CallbackDict({'lol': 'wtf'})
        """
        return cls(dict.fromkeys(iterable, value))


CallbackDict._expose_all(
    '__contains__', '__iter__',
    '__setitem__', '__getitem__', '__delitem__',
    '__eq__', '__ne__',
    'clear', 'copy', 'get', 'items', 'keys', 'pop', 'popitem',
    'setdefault', 'update', 'values',
)


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
        the family is 'Monospace', a monospace font will be used even if
        a font with the name 'monospace' is not available.

        >>> Font(' mONoSpACe   ')
        <BananaGUI font, family='Monospace' size=None>
        >>> Font('Sans')
        <BananaGUI font, family='Sans' size=None>
        """
        if family is not None:
            assert family, "family cannot be empty"
            if family.lower().strip() == 'monospace':
                family = 'Monospace'
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

    def to_string(self) -> str:
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

    def to_translated_string(self) -> str:
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


class Color(collections.namedtuple('Color', 'red green blue')):
    """An immutable color.

    The colors are based on a namedtuple, so they behave a lot like
    (r, g, b) tuples. Actually they are (r, g, b) tuples.
    """

    def __init__(self, red, green, blue):
        """Check the red, green and blue values."""
        # Most of the initialization is done by the namedtuple's
        # __new__. See Color._source.
        for value in (red, green, blue):
            assert value in range(256), "invalid r/g/b value %r" % (value,)

    @property
    def brightness(self) -> float:
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
        Color(red=255, green=255, blue=0)
        >>> Color.from_hex(' #FfFF00   ')
        Color(red=255, green=255, blue=0)
        >>> Color.from_hex('#ff0')
        Color(red=255, green=255, blue=0)
        """
        hexstring = hexstring.strip()
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
    def hex(self) -> str:
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
        Color(red=255, green=255, blue=0)
        >>> Color.from_rgbstring('rG B ( 255 , 100 % ,0) ')
        Color(red=255, green=255, blue=0)
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
    def rgbstring(self) -> str:
        """Convert self to a CSS-compatible color string.

        >>> Color(255, 255, 0).rgbstring
        'rgb(255,255,0)'
        """
        return 'rgb(%d,%d,%d)' % self


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
