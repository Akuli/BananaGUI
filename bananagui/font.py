"""A font class for BananaGUI."""

import collections


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

        >>> Font.from_string('Sans, 16, bold italic')      # doctest: +ELLIPSIS
        Font(family='Sans', size=16, bold=True, italic=True, ...)
        >>> Font.from_string(' Sans ,16,bOlD ItALic ')     # doctest: +ELLIPSIS
        Font(family='Sans', size=16, bold=True, italic=True, ...)
        >>> Font.from_string('Sans, 16')                   # doctest: +ELLIPSIS
        Font(family='Sans', size=16, bold=False, italic=False, ...)
        >>> Font.from_string('default family, default size')
        Font(family=None, size=None, bold=False, italic=False, underline=False)
        """
        assert isinstance(string, str)

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
        # This relies on falsiness of None because family and size are
        # checked in __new__.
        result = [self.family or 'default family',
                  str(self.size or 'default size')]

        attributes = [attribute
                      for attribute in ('bold', 'italic', 'underline')
                      if getattr(self, attribute)]
        if attributes:
            result.append(' '.join(attributes))

        return ', '.join(result)


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
