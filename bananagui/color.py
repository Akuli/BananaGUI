"""This module contains handy color constants and converting functions.

BananaGUI uses case-insensitive 7-character hexadecimal colors, like
``'#ffffff'`` or ``'#fFfFff'``. If you're not familiar with hexadecimal
colors you probably can't guess what ``'#ff0000'`` and ``'#00ff00'``
are. This module allows you to use ``bananagui.Color.RED`` and
``bananagui.Color.GREEN`` instead.

Here's a full list of the color constants:

%(constant-table)s

Rest of this module contains functions for converting colors and
processing hexadecimal colors.
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


def _generate_table():
    names = [name for name in globals() if name.isupper()]
    names.sort()
    lines = [
        "+------------+---------------+",
        "| Name       | Value         |",
        "+============+===============+",
    ]
    for name in names:
        value = globals()[name]
        lines.append("| %-10s | ``'%s'`` |" % (name, value))
        lines.append("+------------+---------------+")
    return '\n'.join(lines)


if __doc__ is not None:
    # Not running with Python's optimizations.
    __doc__ %= {'constant-table': _generate_table()}


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


def rgb2hex(rgb) -> str:
    """Convert an RGB sequence to a hexadecimal color.

    The values of the sequence need to be in ``range(256)``.

    >>> rgb2hex([0, 255, 255])
    '#00ffff'
    """
    return '#%02x%02x%02x' % tuple(rgb)


def hex2rgb(hexcolor: str) -> tuple:
    """Convert a hexadecimal color to an RGB tuple.

    The returned values are always integers in ``range(256)``.

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


# The _number is an integer or float as a group, may end with % or have
# whitespace around it.
_number = r'\s*(\d*\.?\d*%?)\s*'
_rgbstring_patterns = [
    r'^\s*rgb\s*\(' + ','.join([_number] * 3) + r'\)\s*$',   # rgb(R,G,B)
    r'^\s*rgba\s*\(' + ','.join([_number] * 4) + r'\)\s*$',  # rgba(R,G,B,A)
]


def rgbstring2hex(rgbstring: str) -> str:
    """Convert a CSS compatible color string to a hexadecimal color string.

    This supports percents.

    >>> rgbstring2hex('rgb(255,100%,0)')
    '#ffff00'
    >>> rgbstring2hex(' rgb ( 255 ,100%, 0 ) ')
    '#ffff00'
    >>> rgbstring2hex('rgba(255,100%,0,0.5)')  # alpha value is ignored
    '#ffff00'
    """
    for pattern in _rgbstring_patterns:
        match = re.search(pattern, rgbstring)
        if match is None:
            continue
        rgb = []
        for i in (1, 2, 3):
            value = match.group(i)
            if value.endswith('%'):
                rgb.append(float(value.rstrip('%')) / 100 * 255)
            else:
                rgb.append(float(value))
        return rgb2hex(map(int, rgb))
    raise ValueError("invalid RGB color string %r" % (rgbstring,))


def hex2rgbstring(hexcolor: str) -> str:
    """Convert a hexadecimal color string to a CSS compatible color string.

    >>> hex2rgbstring('#ffff00')
    'rgb(255,255,0)'
    """
    return 'rgb(%d,%d,%d)' % hex2rgb(hexcolor)


def brightness(hexcolor: str) -> float:
    """Return the brightness of the color between 0 and 1.

    >>> brightness('#000000')
    0.0
    >>> brightness('#ffffff')
    1.0
    >>> brightness('#333333')
    0.2
    """
    return sum(hex2rgb(hexcolor)) / 3 / 255
