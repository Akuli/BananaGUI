# Copyright (c) 2016-2017 Akuli

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

"""Font-related things for BananaGUI."""

import functools

from bananagui import _get_wrapper, mainloop, types

__all__ = ['get_families']


# The wrapper doesn't need to provide anything for this, it just needs to
# use this with widgets that have a font attribute.

# TODO: update this and use this in rest of BananaGUI.

@types.add_property('family')
@types.add_property('size')
@types.add_property('bold')
@types.add_property('italic')
@types.add_property('underline')
@types.add_property('overline')
class Font:
    """A class that represents a font.

    Unlike in most other GUI toolkits, it's usually a bad idea to
    create a new Font object. Instead, most widgets provide a font
    attribute that can be used to retrieve the widget's current font as
    a Font object and change that.

    The family attribute is the font's family as a string. Usually it's
    a bad idea to use hard-coded font families. If you want to customize
    the fonts it's recommended to allow the users to choose the fonts
    they want to use with a font dialog. If you just want to make a font
    monospaced you can set this to a family called 'Monospace' so the
    default monospace font will be used. The get_families() function
    returns a list of possible family values.

    The size attribute is the font size in pixels. Usually it's a bad
    idea to use hard-coded font families and sizes. If you just want to
    make something bigger, you can do this:

        some_widget.font.size *= 2

    The bold, italic, underline and overline attributes are Booleans.
    """

    def __init__(self, family, size, bold, italic, underline, overline):
        self._family = family
        self._size = size
        self._bold = bold
        self._italic = italic
        self._underline = underline
        self._overline = overline

        # The widget that created the font should add something to
        # this. Everything in this list will be called with the font as
        # the only argument when anything about the font changes.
        self._on_changed = []

    def __repr__(self):
        words = ['family=%r' % self.family, 'size=%r' % self.size]
        for attribute in ('bold', 'italic', 'underline', 'overline'):
            value = getattr(self, attribute)
            if value:
                words.append('%s=%r' % (attribute, value))
        return '<BananaGUI font, %s>' % ' '.join(words)

    def _run_callbacks(self, value):
        for callback in self._on_changed:
            callback(self)

    _set_family = _run_callbacks
    _set_size = _run_callbacks
    _set_bold = _run_callbacks
    _set_italic = _run_callbacks
    _set_underline = _run_callbacks
    _set_overline = _run_callbacks

    def _check_family(self, family):
        assert family in get_families(), "unknown family %r" % (family,)

    def _check_size(self, size):
        assert isinstance(size, int) and size > 0, \
            "font sizes must be positive integers"

    def _check_boolean(self, value):
        assert isinstance(value, bool), "%r is not a Boolean" % (value,)

    _check_bold = _check_boolean
    _check_italic = _check_boolean
    _check_underline = _check_boolean
    _check_overline = _check_boolean


@functools.lru_cache()
def get_families() -> frozenset:
    """Return a frozenset of all avaliable font families."""
    if not mainloop._initialized:
        raise RuntimeError("the mainloop wasn't initialized")

    # The wrapper function can return anything iterable.
    fonts = {'Monospace'}
    fonts.update(_get_wrapper('font:get_families')())
    return frozenset(fonts)
