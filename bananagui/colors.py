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

"""Color converting functions."""

import re


def _rgb2longhex(r, g, b):
    """Create a "long" hexadecimal color from red, green and blue values.

    (255, 255, 255) -> '#ffffff'
    """
    for value in (r, g, b):
        if value not in range(256):
            raise ValueError("invalid r/g/b value {!r}".format(value))
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def _hexregex2longhex(regex, color, converter):
    """Convert a color to rgb using a regex."""
    match = re.search(regex, color)
    if match is None:
        raise ValueError("cannot parse {!r} with regex {}"
                         .format(color, regex))
    r, g, b = map(converter, match.groups())
    return _rgb2longhex(r, g, b)


def get_hexcolor(*color):
    """Convert a color to a hexadecimal color string.

    All of the following will return '#ffffff':
        get_hexcolor('#fFfFFF')
        get_hexcolor('#fff')
        get_hexcolor((255, 255, 255))
        get_hexcolor([255, 255, 255])
        get_hexcolor(255, 255, 255)
        get_hexcolor(255 for i in range(3))
        get_hexcolor('rgb(255,100%,100%)')
    """
    # Accept a sequence of arguments as multiple arguments.
    if len(color) == 1:
        color = color[0]

    if isinstance(color, str):
        if re.search('^#' + '([0-9A-Fa-f])'*3 + '$', color):
            # "Short" hexadecimal color.
            return _hexregex2longhex(
                '^#' + '([0-9A-Fa-f])'*3 + '$',
                color,
                lambda s: int(s*2, 16),
            )
        if re.search('^#' + '([0-9A-Fa-f]{2})'*3 + '$', color):
            # "Long" hexadecimal color.
            return _hexregex2longhex(
                '^#' + '([0-9A-Fa-f]{2})'*3 + '$',
                color,
                lambda s: int(s, 16),
            )
        if re.search('^rgb((d+%?),(d+%?),(d+%?))$', color):
            # "RGB string".
            return _hexregex2longhex(
                '^rgb((d+%?),(d+%?),(d+%?))$',
                color,
                lambda s: int(s[:-1])*255//100 if s.endswith('%') else int(s),
            )

    else:
        # R, G and B values.
        return _rgb2longhex(*color)

    raise ValueError("cannot parse {!r}".format(color))
