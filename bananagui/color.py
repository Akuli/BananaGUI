# Copyright (c) 2016 Akuli

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""A color class and color constants."""

import collections
import re


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


# TODO: Add a BROWN.

BLACK = Color(0, 0, 0)
GRAY = Color(127, 127, 127)
WHITE = Color(255, 255, 255)
RED = Color(255, 0, 0)
ORANGE = Color(255, 127, 0)
YELLOW = Color(255, 255, 0)
GREEN = Color(0, 255, 0)
CYAN = Color(0, 255, 255)
BLUE = Color(0, 0, 255)
PINK = Color(255, 0, 255)


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
