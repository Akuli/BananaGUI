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

import bananagui
from bananagui import _base, utils
from .basewidgets import Child


@utils.baseclass
@bananagui.document_props
class BaseButton(_base.BaseButton, Child):
    """Base for other buttons."""

    on_click = bananagui.BananaSignal(
        'on_click', doc="This is emitted when the button is clicked.")


@bananagui.document_props
class Button(_base.Button, BaseButton):
    """A button that displays text in it."""

    text = bananagui.BananaProperty(
        'text', type=str, default='',
        doc="The text in the button.")


@bananagui.document_props
class ImageButton(_base.ImageButton, BaseButton):
    """A button that displays an image."""
    imagepath = bananagui.BananaProperty.imagepath(
        'imagepath',
        doc="Path to the image that is displayed in the button.")
