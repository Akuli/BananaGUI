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

"""Define structures used in rest of BananaGUI.

Names in this module are also available in bananagui.__init__, so you
don't need to import anything directly from here.
"""


import re

from bananagui.utils import descriptors


# Color parsing functions.

def _regex2hex(regex, string, converter=None):
    """Use a regular expression to parse string into an RGB tuple.

    Optionally, apply a converter to red, green and blue values.
    """
    string = str(string)
    match = re.search(regex, string)
    if match is None:
        raise ValueError("cannot parse %r" % string)
    rgb = match.groups()
    if converter is not None:
        rgb = map(converter, rgb)
    return rgb2hex(*rgb)


def rgb2hex(r, g, b):
    """Create a hexadecimal color string from red, green and blue."""
    r, g, b = map(int, (r, g, b))
    for value in (r, g, b):
        if value not in range(256):
            raise ValueError("invalid rgb value %d" % value)
    return '#%02x%02x%02x' % (r, g, b)


def rgbstring2hex(rgbstring):
    """Convert a CSS-style RGB string like 'rgb(0,0,0)' to hexadecimal.

    Percents are also supported. For example, 'rgb(255,100%,100%)' is
    white.
    """
    return _regex2hex(
        r'^rgb\((\d+%?),(\d+%?),(\d+%?)\)$',
        rgbstring,
        lambda x: int(x[:-1]) * 255 // 100 if x.endswith('%') else x,
    )


def hex2hex(hexstring):
    """Check a hexadecimal color string and format it nicely."""
    hexstring = str(hexstring)
    if len(hexstring) == 4:
        # It's short, like '#fff'.
        hashtag, r, g, b = hexstring
        r, g, b = r * 2, g * 2, b * 2
        hexstring = hashtag + r + g + b
    return _regex2hex(
        r'^#([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})$',
        hexstring,
        lambda value: int(value, 16),
    )


def anything2hex(anything):
    """Attempt to convert a Python object to a hexadecimal color.

    This uses other functions in this module.
    """
    try:
        return 


class Font:
    """A font.

    Family and size can be None, so their default values will be used.
    If the family is 'monospace', a monospace font will be used even if
    a font with the name monospace is not installed.
    """

    family = descriptors.String()
    size = descriptors.NonNegativeIntegerOrNone()
    bold = descriptors.Boolean()
    italic = descriptors.Boolean()
    underline = descriptors.Boolean()

    def __init__(self, family=None, size=None, bold=False, italic=False,
                 underline=False):
        """Initialize the font."""
        self.family = family
        self.size = size
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self._validate()

    def __repr__(self):
        """Return a nice representation of the font."""
        return ('%s(%r, %r, bold=%r, italic=%r, underline=%r)'
                % (type(self).__name__, self.family, self.size,
                   self.bold, self.italic, self.underline))

    @classmethod
    def from_string(cls, string):
        """Parse a font from a string and return it."""
        try:
            # This is not done with a regular expression so that a wrong
            # number of spaces is not going to break this.
            family_and_size, attributes = string.split(',')
            family_and_size = family_and_size.split()
            if family_and_size[-1].isdigit():
                size = int(family_and_size.pop())
            else:
                size = None
            family = ' '.join(family_and_size)
            kwargs = {key.lower(): True for key in attributes.split()}
            return cls(family, size, **kwargs)
        except (TypeError, ValueError, IndexError) as e:
            raise ValueError("invalid font string: %r" % string) from e

    def to_string(self):
        """Convert the font to a string.

        The string can be parsed by from_string.
        """
        result = self.family
        if self.size is not None:
            result += ' '
            result += str(self.size)

        attributes = []
        for attribute in ('bold', 'italic', 'underline'):
            if getattr(self, attribute):
                attributes.append(attribute.capitalize())
        if attributes:
            result += ', '
            result += ' '.join(attributes)
        return result
