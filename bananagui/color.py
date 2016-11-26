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

"""Handy color utilities."""

import re


def hex2rgb(hexcolor):
    """Convert a hexadecimal color to an RGB tuple.

    >>> hex2rgb('#00ffff')
    (0, 255, 255)
    >>> hex2rgb('#0ff')
    (0, 255, 255)
    >>> hex2rgb('#000ffffff')
    (0, 255, 255)
    """
    assert hexcolor.startswith('#'), \
        "hexadecimal colors should start with '#', got %r" % (hexcolor,)
    values = hexcolor[1:]
    assert values and len(values) % 3 == 0, \
        "cannot divide %r into 3 even chunks" % (values,)
    chunksize = len(values) // 3
    if chunksize == 1:
        # It's like '0ff', we need to double everything up so we get
        # '00ffff' because that's the precision we'll go with.
        r, g, b = values
        r *= 2
        g *= 2
        b *= 2
    else:
        # We need to truncate the values to two hexadecimal digits.
        r = values[0:2]
        g = values[chunksize:chunksize+2]
        b = values[chunksize*2:chunksize*2+2]
    return int(r, 16), int(g, 16), int(b, 16)


def rgb2hex(*args):
    """Convert an rgb color to a hexadecimal color.

    The color may be an (r, g, b) sequence or multiple arguments.

    >>> rgb2hex(0, 255, 255)
    '#00ffff'
    >>> rgb2hex([0, 255, 255])
    '#00ffff'
    """
    if len(args) == 1:
        r, g, b = args[0]
    else:
        r, g, b = args
    return '#%02x%02x%02x' % (r, g, b)


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


def rgbstring2hex(rgbstring):
    """Convert a CSS compatible color string to a hexadecimal color string.

    This supports percents.

    >>> rgbstring2hex('rgb(255,100%,0)')
    '#ffff00'
    >>> rgbstring2hex('rG B ( 255 , 100 % ,0) ')
    '#ffff00'
    """
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


def hex2rgbstring(hexcolor):
    """Convert a hexadecimal color string to a CSS compatible color string.

    >>> hex2rgbstring('#ffff00')
    'rgb(255,255,0)'
    """
    return 'rgb(%d,%d,%d)' % hex2rgb(hexcolor)


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
