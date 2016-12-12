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
from bananagui import types
from .basewidgets import Child


# TODO: do we need this?
class BaseLabel(Child):
    """A base class for widgets that are meant for displaying things."""


@types.add_property('text')
class Label(BaseLabel):
    """A widget that displays text.

        ,---------------.
        |  Hello World! |
        `---------------'

    The text is always centered. If you would like to have text that
    aligns to left or right instead, let me know and I'll implement it.

    Attributes:
      text      The text in the label.
    """
    # TODO: Add fonts and colors?

    def __init__(self, parent, text='', **kwargs):
        self._text = ''
        baseclass = bananagui._get_base('widgets.labels:Label')
        self._base = baseclass(self, parent._base)
        super().__init__(parent, **kwargs)
        self.text = text

    def _check_text(self, text):
        assert isinstance(text, str)

    def __repr__(self):
        cls = type(self)
        return '<%s.%s widget, text=%r>' % (
            cls.__module__, cls.__name__, self.text)


@types.add_property('imagepath')
class ImageLabel(BaseLabel):
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
      imagepath     Path to the image displayed in the label or None.
    """

    def __init__(self, parent, imagepath=None, **kwargs):
        self._imagepath = None
        baseclass = bananagui._get_base('widgets.labels:ImageLabel')
        self._base = baseclass(self, parent._base)
        super().__init__(parent, **kwargs)
        self.imagepath = imagepath

    def _check_imagepath(self, path):
        assert path is None or isinstance(path, str)
