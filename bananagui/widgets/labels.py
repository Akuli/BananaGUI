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

"""BananaGUI labels."""

import bananagui
from bananagui import images, types
from .basewidgets import Child


@types.add_property('text', type=str)
@types.add_property('align', choices={bananagui.LEFT, bananagui.CENTER,
                                      bananagui.RIGHT})
class Label(Child):
    """A widget that displays text.

        ,---------------.
        |  Hello World! |
        `---------------'

    Attributes:
      text      The text in the label.
    """
    # TODO: Add fonts and colors?

    def __init__(self, text='', *, align=bananagui.CENTER, **kwargs):
        self._text = ''
        self._align = bananagui.CENTER
        wrapperclass = bananagui._get_wrapper('widgets.labels:Label')
        self._wrapper = wrapperclass(self)
        super().__init__(**kwargs)
        self.text = text
        self.align = align

    def _repr_parts(self):
        return ['text=' + repr(self.text)] + super()._repr_parts()


@types.add_property('image', type=images.Image, allow_none=True)
class ImageLabel(Child):
    r"""A widget that displays an image.

        ,---------------.
        |        __     |
        |    _  / /     |
        |     )/ /      |
        |    /  /_      |
        |   |  |  \     |
        |   |_/         |
        `---------------'

    Attributes:
      image     The bananagui.images.Image in the widget or None.
                Setting this copies the image.
    """

    def __init__(self, image=None, **kwargs):
        self._image = None
        wrapperclass = bananagui._get_wrapper('widgets.labels:ImageLabel')
        self._wrapper = wrapperclass(self)
        super().__init__(**kwargs)
        self.image = image

    def _repr_parts(self):
        return ['image=' + repr(self.image)] + super()._repr_parts()
