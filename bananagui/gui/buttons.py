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

from bananagui import _base, utils
from .basewidgets import Child


class BaseButton(_base.BaseButton, Child):
    """Base class for other buttons.

    Attributes:
      on_click  List of callbacks that are ran when the button is clicked.
    """

    can_focus = True

    def __init__(self, *args, **kwargs):
        self.on_click = []
        super().__init__(*args, **kwargs)


@utils.add_property('text')
class Button(_base.Button, BaseButton):
    """A button that displays text in it.

    Attributes:
      text      The text in the button.
                An empty string by default.
    """

    def __init__(self, *args, **kwargs):
        self._text = ''
        super().__init__(*args, **kwargs)

    def _check_text(self, text):
        assert isinstance(text, str)


@utils.add_property('imagepath')
class ImageButton(_base.ImageButton, BaseButton):
    """A button that displays an image.

    Attributes:
      imagepath     Path to the image displayed in the button or None.
                    None by default.
    """

    def __init__(self, *args, **kwargs):
        self._imagepath = None
        super().__init__(*args, **kwargs)

    def _check_imagepath(self, path):
        assert path is None or isinstance(path, str)
