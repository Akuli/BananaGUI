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


def _is_valid_color(hexcolor):
    """Check if hexcolor is a valid 7-character hexadecimal color.

    BananaGUI uses this internally.

    >>> _is_valid_color('#fFffFf')
    True
    >>> _is_valid_color('#fffgff')
    False
    >>> _is_valid_color('#fff')     # consistency is needed
    False
    >>> _is_valid_color(123)
    False
    """
    if not isinstance(hexcolor, str):
        return False
    return re.search(r'^#[0-9A-Fa-f]{6}$', hexcolor) is not None


def hex2rgb(hexcolor):
    """Convert a hexadecimal color to an RGB tuple.

    The returned values are always integers in range(255).

    >>> hex2rgb('#00ffff')
    (0, 255, 255)
    >>> hex2rgb('#0ff')
    (0, 255, 255)
    >>> hex2rgb('#000ffffff')
    (0, 255, 255)
    """
    if hexcolor == '#' or not hexcolor.startswith('#'):
        raise ValueError("invalid hexadecimal color string %r" % (hexcolor,))
    if len(hexcolor) % 3 != 1:  # 1 is the '#'
        raise ValueError("cannot divide %r into a # and 3 equally "
                         "sized chunks" % (hexcolor,))

    chunksize = len(hexcolor) // 3
    maximum = int('f' * chunksize, 16)
    rgb = []
    for start in range(1, len(hexcolor), chunksize):
        end = start + chunksize
        rgb.append(int(hexcolor[start:end], 16) * 255 // maximum)
    return tuple(rgb)


def rgb2hex(rgb):
    """Convert an RGB sequence to a hexadecimal color.

    The values need to be in range(256).

    >>> rgb2hex([0, 255, 255])
    '#00ffff'
    """
    r, g, b = rgb     # Allow anything iterable of length 3.
    for value in (r, g, b):
        assert value in range(256), "invalid R/G/B value %r" % (value,)
    return '#%02x%02x%02x' % (r, g, b)


def hex2rgbstring(hexcolor):
    """Convert a hexadecimal color string to a CSS compatible color string.

    >>> hex2rgbstring('#ffff00')
    'rgb(255,255,0)'
    """
    return 'rgb(%d,%d,%d)' % hex2rgb(hexcolor)


_number = r'(\d*\.?\d*%?)'  # Integer or float as a group, may end with %.
_rgbstring_patterns = [
    r'^rgb\(' + ','.join([_number] * 3) + r'\)$',   # rgb(R,G,B)
    r'^rgba\(' + ','.join([_number] * 4) + r'\)$',  # rgba(R,G,B,A)
]


def rgbstring2hex(rgbstring):
    """Convert a CSS compatible color string to a hexadecimal color string.

    This supports percents.

    >>> rgbstring2hex('rgb(255,100%,0)')
    '#ffff00'
    >>> rgbstring2hex('rG B ( 255 , 100 % ,0) ')
    '#ffff00'
    >>> rgbstring2hex('rgba(255,100%,0,0.5)')  # alpha value is ignored
    '#ffff00'
    """
    rgbstring = ''.join(rgbstring.split())  # Remove whitespace.
    for pattern in _rgbstring_patterns:
        match = re.search(pattern, rgbstring, flags=re.IGNORECASE)
        if match is None:
            continue
        rgb = []
        for i in (1, 2, 3):
            value = match.group(i)
            if value.endswith('%'):
                rgb.append(int(value[:-1]) * 255 // 100)
            else:
                rgb.append(int(value))
        return rgb2hex(rgb)
    raise ValueError("invalid RGB color string %r" % (rgbstring,))


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
