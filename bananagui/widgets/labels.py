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

from bananagui import _get_wrapper, Align, images, types
from .basewidgets import Child


@types.add_property('text', type=str, doc="The text in the label.")
@types.add_property(
    'align', type=Align,
    doc="""How the text is aligned.

    This needs to be a :class:`bananagui.Align` member.
    """)
class Label(Child):
    """A widget that displays text.

    .. code-block:: none

       ,---------------.
       |  Hello World! |
       `---------------'

    .. seealso:: `Text editing widgets`_.
    """
    # TODO: Add fonts and colors?

    def __init__(self, text='', *, align=Align.CENTER, **kwargs):
        """Initialize the label.

        The align will be converted to a :class:`bananagui.Align` member.
        """
        self._prop_text = ''
        self._prop_align = Align.CENTER
        wrapperclass = _get_wrapper('widgets.labels:Label')
        self._wrapper = wrapperclass(self)
        super().__init__(**kwargs)
        self.text = text
        self.align = Align(align)

    def _repr_parts(self):
        return ['text=' + repr(self.text)] + super()._repr_parts()


@types.add_property(
    'image', type=images.Image, allow_none=True,
    doc="""The image displayed in the button.

    This should be None or a :class:`bananagui.images.Image`.
    """)
class ImageLabel(Child):
    r"""A widget that displays an image.

    .. code-block:: none

       ,---------------.
       |        __     |
       |    _  / /     |
       |     )/ /      |
       |    /  /_      |
       |   |  |  \     |
       |   |_/         |
       `---------------'
    """

    def __init__(self, image=None, **kwargs):
        """Initialize the image label."""
        self._prop_image = None
        wrapperclass = _get_wrapper('widgets.labels:ImageLabel')
        self._wrapper = wrapperclass(self)
        super().__init__(**kwargs)
        self.image = image

    def _repr_parts(self):
        return ['image=' + repr(self.image)] + super()._repr_parts()
