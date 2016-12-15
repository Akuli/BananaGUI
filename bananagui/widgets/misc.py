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
from bananagui import types
from .basewidgets import _Oriented, Child

# TODO: A RadioButton, or _RadioButton and RadioButtonManager.
# TODO: move Checkbox, Radiostuff and stuff like that to a checkboxes.py?


@types.add_property('text')
@types.add_property('checked', add_changed=True)
class Checkbox(Child):
    """A widget that can be checked.

        ,-------------------.
        |   |   Check me!   |
        `-------------------'

        ,-------------------.
        | X |  Uncheck me!  |
        `-------------------'

    The Checkbox widget has nothing to do with the Box widget.

    Attributes:
      text                  The text next to the checkbox.
      checked               True if the checkbox is checked currently.
                            False by default.
      on_checked_changed    List of callbacks that are called on (un)check.
    """

    can_focus = True

    def __init__(self, parent, text='', *, checked=False, **kwargs):
        self._text = ''
        self._checked = False
        baseclass = bananagui._get_base('widgets.misc:Checkbox')
        self._base = baseclass(self, parent._base)
        super().__init__(parent, **kwargs)
        self.text = text
        self.checked = checked

    def _repr_parts(self):
        return [
            'text=' + repr(self.text),
            'checked=' + repr(self.checked),
        ] + super()._repr_parts()

    def _check_text(self, text):
        assert isinstance(text, str)

    def _check_checked(self, checked):
        assert isinstance(checked, bool)


class Dummy(Child):
    """An empty widget.

        ,-----------.
        |           |
        |           |
        `-----------'

    This is useful for creating layouts with empty space that must be
    filled with something. See Child's documentation for more info.
    """

    def __init__(self, parent, **kwargs):
        baseclass = bananagui._get_base('widgets.misc:Dummy')
        self._base = baseclass(self, parent._base)
        super().__init__(parent, **kwargs)


class Separator(_Oriented, Child):
    """A horizontal or vertical line.

                        ||
            Widget 1    ||
        ================||  Widget 3
            Widget 2    ||
                        ||

    Usually there's no need to add separators between widgets, but they
    are sometimes useful.
    """

    def __init__(self, parent, *, orientation, **kwargs):
        # Make the separator expand correctly by default.
        if orientation == bananagui.HORIZONTAL:
            kwargs.setdefault('expand', (True, False))
        if orientation == bananagui.VERTICAL:
            kwargs.setdefault('expand', (False, True))
        baseclass = bananagui._get_base('widgets.misc:Separator')
        self._base = baseclass(self, parent._base, orientation)
        self.orientation = orientation
        super().__init__(parent, **kwargs)
