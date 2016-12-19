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

"""Button widgets."""

import bananagui
from bananagui import types
from .basewidgets import Child


@types.add_property('text', type=str)
class Button(Child):
    r"""A button that displays text in it.

         _______________
        |,--------------\
        ||   Click me!  |
        `---------------'

    Attributes:
      text      The text in the button.
                An empty string by default.
      on_click  List of callbacks that are ran when the button is
                clicked.
    """

    can_focus = True

    def __init__(self, parent, text='', **kwargs):
        self._text = ''
        self.on_click = []
        baseclass = bananagui._get_base('widgets.buttons:Button')
        self._base = baseclass(self, parent._base)
        super().__init__(parent, **kwargs)
        self.text = text

    def _repr_parts(self):
        return ['text=' + repr(self.text)] + super()._repr_parts()


@types.add_property('imagepath', type=str, allow_none=True)
class ImageButton(Child):
    r"""A button that displays an image.

         _______________
        |.--------------\
        ||       __     |
        ||   _  / /     |
        ||    )/ /      |
        ||   /  /_      |
        ||  |  |  \     |
        ||  |_/         |
        `---------------'

    Attributes:
      imagepath     Path to the image displayed in the button or None.
                    None by default.
      on_click      List of callbacks that are ran when the button is
                    clicked.
    """

    can_focus = True

    def __init__(self, parent, imagepath=None, **kwargs):
        self._imagepath = None
        self.on_click = []
        baseclass = bananagui._get_base('widgets.buttons:ImageButton')
        self._base = baseclass(self, parent._base)
        super().__init__(parent, **kwargs)
        self.imagepath = imagepath

    def _repr_parts(self):
        return ['imagepath=' + repr(self.imagepath)] + super()._repr_parts()
