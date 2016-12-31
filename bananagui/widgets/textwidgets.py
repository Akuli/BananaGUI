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
from bananagui import types
from .basewidgets import Child


@types.add_property('text', type=str, add_changed=True)
class TextBase(Child):
    """A base class for text editing widgets.

    Setting grayed_out to True means that the user can't edit the text.

    Attributes:
      text              The text in the widget.
      on_text_changed   A callback that runs when the text changes.
    """
    # TODO: Add fonts and colors.

    can_focus = True

    def __init__(self, text='', **kwargs):
        self._text = ''
        super().__init__(**kwargs)
        self.text = text

    def select_all(self):
        """Select all text in the widget."""
        self._wrapper.select_all()


@types.add_property('secret', type=bool)
class Entry(TextBase):
    """A one-line text widget.

        ,-----------------------.
        | Enter something...    |
        `-----------------------'

    Attributes:
      secret    True if the text is hidden with stars or balls.
                It's also impossible to copy-paste content from a
                secret entry. This is useful for asking passwords.
    """

    def __init__(self, text='', *, secret=False, **kwargs):
        self._secret = False
        wrapperclass = bananagui._get_wrapper('widgets.textwidgets:Entry')
        self._wrapper = wrapperclass(self)
        super().__init__(text=text, **kwargs)
        self.secret = secret

    def _repr_parts(self):
        parts = ['text=%r' % self.text] + super()._repr_parts()
        if self.secret:
            parts.append('secret=True')
        return parts


# TODO: text wrapping.
# TODO: text alignment?
# TODO: make this behave like a list of lines.
@types.add_property('tab', type=str)
class TextEdit(TextBase):
    """A multiline text widget.

        ,-----------.
        | Line 0    |
        | Line 1    |
        | Line 2    |
        | Line 3    |
        |           |
        `-----------'

    Attributes:
      tab       The character that pressing tab inserts.
    """

    def __init__(self, text='', *, tab='\t', **kwargs):
        self._tab = '\t'
        wrapperclass = bananagui._get_wrapper('widgets.textwidgets:TextEdit')
        self._wrapper = wrapperclass(self)
        super().__init__(text=text, **kwargs)
        self.tab = tab

    # We can't add the whole text here because it would be too long.
    def _repr_parts(self):
        linecount = self.text.count('\n') + 1
        amount = "one line" if linecount == 1 else "%d lines" % linecount
        return super()._repr_parts() + ["contains %s of text" % amount]
