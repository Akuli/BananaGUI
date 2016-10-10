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

from bananagui import _base, Property, bananadoc
from bananagui.utils import baseclass
from .bases import Child


@baseclass
@bananadoc
class TextBase(_base.TextBase, Child):
    """A base class for text editing widgets."""

    # TODO: Add fonts and colors.
    text = Property('text', type=str, default='',
                    doc="Text in the entry.")
    read_only = Property(
        'read_only', type=bool, default=True,
        doc="True if the content of the widget cannot be edited.")

    # This is overrided just to make sure it has a docstring.
    def select_all(self):
        """Select all text in the widget."""
        super().select_all()


@bananadoc
class Entry(_base.Entry, TextBase):
    """A one-line text widget."""

    hidden = Property(
        'hidden', type=bool, default=False,
        doc="True if the entry's content is hidden with asterisks or balls.")


@bananadoc
class PlainTextView(_base.PlainTextView, TextBase):
    """A multiline text widget."""

    tab_inserts = Property(
        'tab_inserts', type=str, default='\t',
        doc="The character(s) that will be inserted when tab is pressed.")

    def _bananagui_set_text(self, text):
        old_text = self['text']

        # The changed signal needs to be emitted once only.
        with self.text.changed.blocked():
            self.clear()
            if text:
                self.append_text(text)
        self.text.changed.emit(old_value=old_text, new_value=text)

    def clear(self):
        """Remove everything from the textview."""
        super().clear()
        # The GUI toolkit's callback updates the text property
        # automatically.

    def append_text(self, text: str):
        """Add text to the end of what is already in the text widget."""
        super().append_text(text)
        # The GUI toolkit's callback updates the text property
        # automatically.
