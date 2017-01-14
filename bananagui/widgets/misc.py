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

"""Miscellaneous widgets."""

import bananagui
from bananagui import types
from .basewidgets import Child

# TODO: A RadioButton, or _RadioButton and RadioButtonManager.
# TODO: move Checkbox, Radiostuff and stuff like that to a checkboxes.py?


@types.add_property('text', type=str, doc="The text next to the checkmark.")
@types.add_property('checked', type=bool, add_changed=True,
                    doc="True if the checkbox is currently checked.")
class Checkbox(Child):
    """A widget that can be checked.

        ,-------------------.
        |   |   Check me!   |
        `-------------------'

        ,-------------------.
        | X |  Uncheck me!  |
        `-------------------'

    The Checkbox widget has nothing to do with the Box widget.
    """

    can_focus = True

    def __init__(self, text='', *, checked=False, **kwargs):
        self._text = ''
        self._checked = False
        wrapperclass = bananagui._get_wrapper('widgets.misc:Checkbox')
        self._wrapper = wrapperclass(self)
        super().__init__(**kwargs)
        self.text = text
        self.checked = checked

    def _repr_parts(self):
        return ['text=%r' % self.text,
                'checked=%r' % self.checked] + super()._repr_parts()


class Dummy(Child):
    """An empty widget.

        ,-----------.
        |           |
        |           |
        `-----------'

    This is useful for creating layouts with empty space that must be
    filled with something. See Child's documentation for more info.
    """

    def __init__(self, **kwargs):
        wrapperclass = bananagui._get_wrapper('widgets.misc:Dummy')
        self._wrapper = wrapperclass(self)
        super().__init__(**kwargs)


class Separator(Child):
    """A horizontal or vertical line.

                        ||
            Widget 1    ||
        ================||  Widget 3
            Widget 2    ||
                        ||

    Usually there's no need to add separators between widgets, but they
    are sometimes useful.

    Attributes:
      orient    The orient set on initialization, converted to a
                bananagui.Orient.
    """

    def __init__(self, orient=bananagui.HORIZONTAL, **kwargs):
        self.__orient = bananagui.Orient(orient)
        # Make the separator expand correctly by default.
        if self.__orient == bananagui.HORIZONTAL:
            kwargs.setdefault('expand', (True, False))
        if self.__orient == bananagui.VERTICAL:
            kwargs.setdefault('expand', (False, True))
        wrapperclass = bananagui._get_wrapper('widgets.misc:Separator')
        self._wrapper = wrapperclass(self, self.__orient)
        super().__init__(**kwargs)

    def _repr_parts(self):
        parts = super()._repr_parts()
        if self.orient == bananagui.VERTICAL:
            # Not the default.
            parts.insert(0, 'orient=bananagui.VERTICAL')
        return parts

    @property
    def orient(self):
        return self.__orient
