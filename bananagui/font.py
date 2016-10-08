"""A font class for BananaGUI."""

import operator


class Font:
    """An immutable font type.

    >>> Font().bold = True
    Traceback (most recent call last):
      ...
    AttributeError: can't set attribute

    Fonts can also be stored in strings using from_string() and
    to_string().

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
        <BananaGUI font family='monospace' size=None>
        >>> Font('Sans')
        <BananaGUI font family='Sans' size=None>
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
        return '<BananaGUI font %s>' % ' '.join(words)

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
        <BananaGUI font family='Sans' size=16 bold=True italic=True>
        >>> Font.from_string(' Sans ,16,bOlD ItALic ')
        <BananaGUI font family='Sans' size=16 bold=True italic=True>
        >>> Font.from_string('Sans, 16')
        <BananaGUI font family='Sans' size=16>
        >>> Font.from_string('default family, 16')
        <BananaGUI font family=None size=16>
        >>> Font.from_string('default family, default size')
        <BananaGUI font family=None size=None>
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
        result = []
        if self.family is None:
            result.append('default family')
        else:
            result.append(self.family)
        if self.size is None:
            result.append('default size')
        else:
            result.append(str(self.size))
        attributes = [attribute
                      for attribute in ('bold', 'italic', 'underline')
                      if getattr(self, attribute)]
        if attributes:
            result.append(' '.join(attributes))
        return ', '.join(result)


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
