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

import os

from bananagui import _base
from bananagui.types import Property, bananadoc
from .bases import ChildBase


@bananadoc
class LabelBase(_base.LabelBase, ChildBase):
    """A label base class."""


@bananadoc
class Label(_base.Label, LabelBase):
    """A label with text in it."""

    # TODO: Add fonts and colors?
    text = Property('text', required_type=str, default='',
                    doc="Text in the label.")


@bananadoc
class ImageLabel(_base.ImageLabel, LabelBase):
    """A label that contains an image."""
    imagepath = Property(
        'imagepath', required_type=str, allow_none=True, default=None,
        doc="""Path to an image file.

        Supported filetypes depend on the GUI toolkit. I recommend using
        `.png` and `.jpg` images because they are well supported by most
        GUI toolkits.
        """)

    def _bananagui_set_path(self, path):
        assert path is None or os.path.isfile(path)
        super()._bananagui_set_path(path)
