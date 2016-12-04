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

"""Handy color utilities.

BananaGUI uses case-insensitive 7-character hexadecimal colors, like
'#ffffff' or '#fFfFff'. This module provides functions for processing
hexadecimal colors and converting colors between hexadecimal colors and
other standards.
"""

import re


BLACK = '#000000'
BROWN = '#996600'
GRAY = '#7f7f7f'
WHITE = '#ffffff'
RED = '#ff0000'
ORANGE = '#ff7f00'
YELLOW = '#ffff00'
GREEN = '#00ff00'
CYAN = '#00ffff'
BLUE = '#0000ff'
PINK = '#ff00ff'


# def _is7charhex(hexcolor):
#    """Check if hexcolor is a valid 7-character hexadecimal color.
#
#    BananaGUI uses this internally.
#    """
#    return re.search(r'^#[0-9a-f]{6}$', hexcolor) is not None


def hex2rgb(hexcolor, precision=2):
    """Convert a hexadecimal color to an RGB tuple.

    If precision is None, it will be guessed based on the color.

    >>> hex2rgb('#00ffff')
    (0, 255, 255)
    >>> hex2rgb('#0ff')
    (0, 255, 255)
    >>> hex2rgb('#000ffffff')
    (0, 255, 255)
    """
    # It must start with '#' but it must contain more than just the '#'.
    assert hexcolor.startswith('#'), \
        "invalid hexadecimal color string %r" % (hexcolor,)
    assert hexcolor != '#', "'#' is not a valid hexadecimal color"

    values = hexcolor[1:]
    assert len(values) % 3 == 0, \
        "cannot divide %r into 3 even chunks" % (values,)
    chunksize = len(values) // 3

    maximum = int('f' * chunksize, 16)
    rgb = []
    for start in range(0, len(values), chunksize):
        end = start + chunksize
        string = values[start:end]
        number = int(string, 16) * 255 // maximum
        rgb.append(number)
    return tuple(rgb)


def rgb2hex(rgb, maxvalue=255):
    """Convert an RGB sequence to a hexadecimal color.

    >>> rgb2hex([0, 255, 255])
    '#00ffff'
    >>> rgb2hex([0, 0.5, 0.5], maxvalue=0.5)
    '#00ffff'
    """
    r, g, b = rgb     # Allow anything iterable of length 3.
    rgb = []
    for value in (r, g, b):
        number = int(value / maxvalue * 255)
        rgb.append(number)
    return '#%02x%02x%02x' % tuple(rgb)


def hex2rgbstring(hexcolor):
    """Convert a hexadecimal color string to a CSS compatible color string.

    >>> hex2rgbstring('#ffff00')
    'rgb(255,255,0)'
    """
    return 'rgb(%d,%d,%d)' % hex2rgb(hexcolor)


def rgbstring2hex(rgbstring):
    """Convert a CSS compatible color string to a hexadecimal color string.

    This supports percents.

    >>> rgbstring2hex('rgb(255,100%,0)')
    '#ffff00'
    >>> rgbstring2hex('rG B ( 255 , 100 % ,0) ')
    '#ffff00'
    """
    # TODO: GTK+ style 'rgba(...)' strings.
    match = re.search(
        r'^rgb\((\d+%?),(\d+%?),(\d+%?)\)$',
        ''.join(rgbstring.split()),  # Remove whitespace.
        flags=re.IGNORECASE,
    )
    assert match is not None, "invalid RGB color string %r" % (rgbstring,)

    rgb = []
    for value in match.groups():
        if value.endswith('%'):
            rgb.append(int(value[:-1]) * 255 // 100)
        else:
            rgb.append(int(value))
    return rgb2hex(rgb)


def clean_hex(hexcolor):
    """Convert any hexadecimal color string to '#RRGGBB'.

    Arguments are handled similarly to hex2rgb.

    >>> clean_hex('#00ffff')
    '#00ffff'
    >>> clean_hex('#0ff')
    '#00ffff'
    >>> clean_hex('#000ffffff')
    '#00ffff'
    """
    return rgb2hex(hex2rgb(hexcolor))


def brightness(hexcolor):
    """Return the brightness of the color between 0 and 1.

    >>> brightness('#000000')
    0.0
    >>> brightness('#ffffff')
    1.0
    >>> brightness('#333333')
    0.2
    """
    return sum(hex2rgb(hexcolor)) / 3 / 255


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
