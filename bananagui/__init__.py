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

"""Simple wrapper for GUI frameworks.

With BananaGUI, it's possible to write some code, and then run the same
code on any supported GUI toolkit, like tkinter, PyQt or GTK+.

To get started with using BananaGUI, get a GUI toolkit wrapper with the
get() function. For example, gui = bananagui.get('tkinter'). The
wrappers come from bananagui.wrappers, so you can open the location of
that module to see which wrappers BananaGUI comes with.

BananaGUI should also come with an example directory with instructions
for running the examples in it, and some markdown files with
descriptions about the examples.
"""

from collections import namedtuple
import importlib
import re


# Constants
# ~~~~~~~~~

HORIZONTAL = 'h'
VERTICAL = 'v'

BLACK = '#000000'
GRAY = '#7f7f7f'
WHITE = '#ffffff'
RED = '#ff0000'
ORANGE = '#ff7f00'
YELLOW = '#ffff00'
GREEN = '#00ff00'
CYAN = '#00ffff'
BLUE = '#0000ff'
PINK = '#ff00ff'


# The get_wrapper() function
# ~~~~~~~~~~~~~~~~~~~~~~~~~~

_WRAPPER_SUBMODULES = (
    '%s.buttons',
    '%s.labels',
    '%s.layouts',
    '%s.windows',
)


def get_wrapper(*wrappernames):
    """Attempt to return a GUI toolkit wrapper from wrappernames.

    The first one is returned, and if it fails the next one is, and so
    on. If no wrappers can be imported, an ImportError is raised.

    Example:
        >>> import bananagui
        >>> bananagui.get('bananagui.wrappers.tkinter')
        <module 'bananagui.wrappers.tkinter' from '...'>
    """
    if not wrappernames:
        raise ValueError("no toolkit names were given")
    for name in wrappernames:
        try:
            # Importing these submodules attaches them to the main
            # wrapper module.
            for module in _WRAPPER_SUBMODULES:
                importlib.import_module(module % name)
            return importlib.import_module(name)
        except ImportError:
            pass
    raise ImportError("cannot import any of the requested toolkits")


# Color converters
# ~~~~~~~~~~~~~~~~

_COLOR_REGEXES_AND_CONVERTERS = [
    # 4-character hexadecimal colors.
    (r'^#' + r'([0-9A-Fa-f])' * 3 + r'$',
     lambda s: int(s * 2, 16)),

    # 7-character hexadecimal colors.
    (r'^#' + r'([0-9A-Fa-f]{2})' * 3 + r'$',
     lambda s: int(s, 16)),

    # 'rgb(r,g,b)' color strings, supports percents.
    (r'^rgb\((\d+%?),(\d+%?),(\d+%?)\)$',
     lambda s: int(s[:-1]) * 255 // 100 if s.endswith('%') else int(s)),
]


def color2rgb(color):
    """Convert a color to an RGB tuple.

    This is used internally in BananaGUI, so if this can convert your
    color correctly, then BananaGUI should also be able to do that.

    Example:
        >>> get_hexcolor('#fFfFFF')
        (255, 255, 255)
        >>> get_hexcolor('#fff')
        (255, 255, 255)
        >>> get_hexcolor((255, 255, 255))
        (255, 255, 255)
        >>> get_hexcolor([255, 255, 255])
        (255, 255, 255)
        >>> get_hexcolor(255 for i in range(3))
        (255, 255, 255)
        >>> get_hexcolor('rgb(255,100%,100%)')
        (255, 255, 255)
    """
    if isinstance(color, str):
        # Use a regex.
        for regex, converter in _COLOR_REGEXES_AND_CONVERTERS:
            match = re.search(regex, color)
            if match is not None:
                r, g, b = map(converter, match.groups())
                break
        else:
            raise ValueError("cannot parse %r" % color)
    else:
        # Red, green and blue values.
        r, g, b = map(int, color)

    for value in (r, g, b):
        if value not in range(256):
            raise ValueError("invalid r/g/b value %r" % (value,))
    return r, g, b


def color2hex(color):
    """Convert color to a hexadecimal color string like '#ffffff'.

    This can convert from everything that convert2rgb can.
    """
    return '#%02x%02x%02x' % color2rgb(color)


# The Font class
# ~~~~~~~~~~~~~~

class Font(namedtuple('Font', 'family size bold italic underline')):
    """A font.

    Family and size can be None, so their default values will be used.
    If the family is 'monospace' (case-sensitive), a monospace font
    will be used even if a font with the name monospace is not
    installed.

    The fonts can also be stored in strings. They are comma-separated
    lists of family, size and bold/italic/underline attributes. For
    example, 'Sans, 16, Bold Italic'. Missing attributes are assumed to
    be empty strings, and empty family/size strings will be converted
    to None. '' is the default font with the default size.
    """

    def __new__(cls, family=None, size=None, bold=False,
                italic=False, underline=False):
        """Create a new font."""
        return super().__new__(
            cls,
            None if family is None else str(family),
            None if size is None else int(size),
            bool(bold),
            bool(italic),
            bool(underline),
        )

    @classmethod
    def from_string(cls, string):
        """Parse a font from a string and return it."""
        try:
            while string.count(',') < 2:
                # The string does not have something required. Assume
                # the missing values are empty strings.
                string += ','
            family, size, attributes = string.split(',')
            family = family.strip() or None
            size = int(size) if size.strip() else None
            attributes = {key.lower(): True for key in attributes.split()}
            return cls(family, size, **attributes)
        except (AttributeError, IndexError, TypeError, ValueError) as e:
            raise ValueError("invalid font string %r" % (string,)) from e

    def to_string(self):
        """Convert the font to a string.

        The string can be parsed by from_string.
        """
        family = self.family or ''
        size = str(self.size or '')
        attributes = ' '.join(a.capitalize()
                              for a in ('bold', 'italic', 'underline')
                              if getattr(self, a))
        return ', '.join([family, size, attributes]).rstrip(', ')
