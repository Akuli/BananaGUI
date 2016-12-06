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

"""Miscellaneous widgets."""

import bananagui
from bananagui import utils
from .basewidgets import _Oriented, Child
from .. import mainloop

_base = bananagui._get_base('widgets.misc')

# TODO: A RadioButton, or _RadioButton and RadioButtonManager.
# TODO: move Checkbox, Radiostuff and everything else to a checkboxes.py?


@utils.add_property('text')
@utils.add_property('checked', add_changed=True)
class Checkbox(_base.Checkbox, Child):
    """A widget that can be checked.

    The Checkbox widget has nothing to do with the Box widget.

    Attributes:
      text                  The text next to the checkbox.
      checked               True if the checkbox is checked currently.
                            False by default.
      on_checked_changed    List of callbacks that are called on (un)check.
    """

    can_focus = True

    def __init__(self, *args, **kwargs):
        self._text = ''
        self._checked = False
        super().__init__(*args, **kwargs)

    def _check_text(self, text):
        assert isinstance(text, str)

    def _check_checked(self, checked):
        assert isinstance(checked, bool)


class Dummy(_base.Dummy, Child):
    """An empty widget.

    This is useful for creating layouts with empty space that must be
    filled with something.
    """


class Separator(_Oriented, _base.Separator, Child):
    """A horizontal or vertical line."""

    def __init__(self, parent, *, orientation, **kwargs):
        # Make the separator expand correctly by default.
        if orientation == bananagui.HORIZONTAL:
            kwargs.setdefault('expand', (True, False))
        if orientation == bananagui.VERTICAL:
            kwargs.setdefault('expand', (False, True))
        super().__init__(parent, orientation=orientation, **kwargs)


def set_clipboard_text(text):
    """Set text to the clipboard."""
    assert mainloop._initialized
    assert isinstance(text, str)
    _base.set_clipboard_text(text)


def get_clipboard_text():
    """Return the text that is currently on the clipboard.

    The returned value is an empty string if there is no text on the
    clipboard.
    """
    assert mainloop._initialized
    return _base.get_clipboard_text()


font_family_cache = []


def get_font_families():
    """Return a list of all avaliable font families as strings."""
    if not font_family_cache:
        # This is converted to a set to make sure that we don't get any
        # duplicates. The base function can return anything iterable.
        font_family_cache.extend(set(_base.get_font_families()))
        font_family_cache.sort()  # Undefined order wouldn't be nice.
    return font_family_cache
