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

"""Base classes for GUI toolkit wrappers."""

from functools import partial
from gettext import gettext as _

from bananagui import _base, bananadoc, Color, Font, Property, BLACK
from . import window
from .window import BaseWindow, Window

try:
    _fontdialog = _base.fontdialog
except AttributeError:
    from bananagui.bases.defaults import fontdialog as _fontdialog


@bananadoc
class Dialog(_base.Dialog, BaseWindow):
    """A window that has a parent window.

    This class takes a parentwindow argument on initialization. The
    parent window must be an instance of Window and it may be centered
    over the parent window, it may be modal or whatever the real GUI
    toolkit supports. It's None by default.
    """

    title = Property('title', type=str, default="BananaGUI Dialog",
                     doc="The title of the window.")
    parentwindow = Property('parentwindow', type=Window, settable=False,
                            doc="The parent window set on initialization.")

    def __init__(self, parentwindow: window.Window, **kwargs):
        self.parentwindow.raw_set(parentwindow)
        super().__init__(**kwargs)


def messagedialog(icon, parentwindow: window.Window, *, text: str,
                  title: str = None, buttons: list = None,
                  defaultbutton: str = None) -> str:
    """Display a message dialog.

    icon should be 'info', 'question', 'warning' or 'error'.

    The buttons argument should be a sequence of button texts that will
    be added to the dialog. It defaults to "OK" translated with
    gettext.gettext in a list.

    The button with defaultbutton as its text will have keyboard focus
    by default. If defaultbutton is not set, the first button will be
    used.

    The text argument is the text that will be shown in the dialog. If
    title is not given, the dialog's title will be the same as
    parentwindow's title.

    The text of the clicked button is returned, or None if the user
    closed the dialog.
    """
    assert icon in {'info', 'question', 'warning', 'error'}

    if title is None:
        title = parentwindow['title']

    if buttons is None:
        buttons = [_("OK")]
    assert buttons, "at least one button is required"

    if defaultbutton is None:
        defaultbutton = buttons[0]
    assert defaultbutton in buttons

    return _base.messagedialog(icon, parentwindow, text, title,
                               buttons, defaultbutton)


# The bases don't need to define these.
infodialog = partial(messagedialog, 'info')
questiondialog = partial(messagedialog, 'question')
warningdialog = partial(messagedialog, 'warning')
errordialog = partial(messagedialog, 'error')


def colordialog(parentwindow: Window, *, default: Color = BLACK,
                title: str = None) -> Color:
    """Ask a color from the user.

    This returns the new color, or None if the user canceled the dialog.
    """
    if title is None:
        title = parentwindow['title']
    return _base.colordialog(parentwindow, default, title)


def fontdialog(parentwindow: Window, *, default: Font = Font(),
               title: str = None) -> Font:
    """Ask a font from the user.

    This returns the new font, or None if the user canceled the dialog.
    """
    if title is None:
        title = parentwindow['title']
    return _fontdialog(parentwindow, default, title)
