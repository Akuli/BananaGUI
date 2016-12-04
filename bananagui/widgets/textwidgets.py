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

"""Widgets that contain text."""

import bananagui
from bananagui import utils
from .basewidgets import Child

_base = bananagui._get_base('widgets.textwidgets')


@utils.add_property('text', add_changed=True)
class TextBase(_base.TextBase, Child):
    """A base class for text editing widgets.

    Setting grayed_out to True means that the user can't edit the text.

    Attributes:
      text              The text in the widget.
      on_text_changed   List of callbacks that run when the text changes.
    """
    # TODO: Add fonts and colors.

    can_focus = True

    def __init__(self, *args, **kwargs):
        self._text = ''
        super().__init__(*args, **kwargs)

    def _check_text(self, text):
        assert isinstance(text, str)

    def select_all(self):
        """Select all text in the widget."""
        self._select_all()


@utils.add_property('secret')
class Entry(_base.Entry, TextBase):
    """A one-line text widget.

    Attributes:
      secret    True if the text is hidden with stars or balls.
                It's also impossible to copy-paste content from a
                secret entry. This is useful for asking passwords.
    """

    def __init__(self, *args, **kwargs):
        self._secret = False
        super().__init__(*args, **kwargs)

    def _check_secret(self, secret):
        assert isinstance(secret, bool)


# TODO: text wrapping.
# TODO: text alignment?
@utils.add_property('tab')
class TextEdit(_base.TextEdit, TextBase):
    """A multiline text widget.

    Attributes:
      tab       The character that pressing tab inserts.
    """

    def __init__(self, *args, **kwargs):
        self._tab = '\t'
        super().__init__(*args, **kwargs)

    def _check_tab(self, tab):
        assert isinstance(tab, str)
