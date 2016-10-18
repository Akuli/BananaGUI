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
from bananagui import _base, utils
from . import bases


@utils.baseclass
@bananagui.bananadoc
class BaseLabel(_base.BaseLabel, bases.Child):
    """A label base class."""


@bananagui.bananadoc
class Label(_base.Label, BaseLabel):
    """A label with text in it.

    Currently the text is always centered.
    """
    # TODO: add an alignment thing? Currently the text in the labels is
    # always centered.
    # TODO: Add fonts and colors?
    text = bananagui.Property('text', type=str, default='',
                              doc="Text in the label.")


@bananagui.bananadoc
class ImageLabel(_base.ImageLabel, BaseLabel):
    """A label that contains an image."""
    imagepath = bananagui.Property.imagepath(
        'imagepath', doc="Path to an image that will be displayed.")
