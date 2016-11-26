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

from gi.repository import Gtk, Gdk

from . import orientations


class Checkbox:

    def __init__(self, parent, **kwargs):
        self.real_widget = Gtk.CheckButton()
        self.real_widget.connect('notify::active', self._do_check)
        super().__init__(parent, **kwargs)

    def _do_check(self, real_widget, gparam):
        self.checked = real_widget.get_active()

    def _set_text(self, text):
        self.real_widget.set_label(text)

    def _set_checked(self, checked):
        self.real_widget.set_active(checked)


class Dummy:

    def __init__(self, parent, **kwargs):
        self.real_widget = Gtk.Label()
        super().__init__(parent, **kwargs)


class Separator:

    def __init__(self, parent, **kwargs):
        gtk_orientation = orientations[self.orientation]
        self.real_widget = Gtk.Separator(orientation=gtk_orientation)
        super().__init__(parent, **kwargs)


_clipboard = None


def _init_clipboard():
    global _clipboard
    if _clipboard is None:
        _clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)


def set_clipboard_text(text):
    _init_clipboard()
    _clipboard.set_text(text, -1)
    _clipboard.store()


def get_clipboard_text():
    _init_clipboard()
    # clipboard.wait_for_text() doesn't block if there's no text on the
    # clipboard, it returns None.
    result = _clipboard.wait_for_text()
    if result is None:
        return ''
    return result


def get_font_families():
    # Based on http://zetcode.com/gui/pygtk/pango/
    widget = Gtk.Label()
    context = widget.create_pango_context()
    return (family.get_name() for family in context.list_families())
