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

from bananagui import types


class EditableBase:
    """A base class for Entry and TextView.

    Properties:
        text            RWC
            The text in the entry.
            An empty string by default.
        read_only       RW
            True if the content of the widget cannot be edited.
            False by default.
    """

    # TODO: Add fonts and colors.
    _bananagui_bases = ('ChildBase',)
    text = types.Property('text', required_type=str, default='')
    read_only = types.Property('read_only', required_type=bool,
                               default=True)

    def select_all(self):
        """Select all text in the widget."""
        super().select_all()


class Entry:
    """A one-line text widget.

    Properties:
        hidden          RW
            True if the entry's content is hidden with asterisks or balls.
            False by default.
    """

    _bananagui_bases = ('EditableBase',)
    hidden = types.Property('hidden', required_type=bool, default=False)


class PlainTextView:
    """A multiline text widget.

    Properties:
        tab_inserts     RW
            The character(s) that will be inserted when tab is pressed.
            '\t' by default.
    """

    _bananagui_bases = ('EditableBase',)
    tab_inserts = types.Property('tab_inserts', required_type=str,
                                 default='\t')

    def _bananagui_set_text(self, text):
        old_text = self['text']
        with self.blocked('text.changed'):
            self.clear()
            if text:
                self.append_text(text)
        self.emit('text.changed', old_value=old_text, new_value=text)

    def clear(self):
        """Remove everything from the textview."""
        super().clear()
        self.raw_set('text', '')

    def append_text(self, text):
        """Add text to the end of what is already in the text widget."""
        if not isinstance(text, str):
            raise TypeError("expected a string, got %r" % (text,))
        super().append_text(text)
        self.raw_set('text', self['text'] + text)
