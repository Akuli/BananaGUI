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

"""Simple message box functions."""

from gettext import gettext as _

import bananagui
from bananagui import color, widgets

_base = bananagui._get_base('msgbox')


def _messagedialog(function):
    """Return a new message dialog function."""
    doc = function.__doc__
    if doc is not None:
        # Not running with Python's optimizations.
        doc += """

        The buttons argument should be a sequence of button texts that
        will be added to the dialog. It defaults to "OK" translated with
        gettext.gettext in a list.

        The button with defaultbutton as its text will have keyboard
        focus by default. If defaultbutton is None and there's one
        button the defaultbutton defaults to it, otherwise there will
        be no default button.

        The text argument is the text that will be shown in the dialog.
        If title is not given, the dialog's title will be the same as
        parentwindow's title.

        The text of the clicked button is returned, or None if the
        dialog is closed. Note that the dialog doesn't have an icon on
        some GUI toolkits.
        """

    def result(parentwindow, message, *, title=None, buttons=None,
               defaultbutton=None):
        assert isinstance(parentwindow, widgets.Window)

        if title is None:
            title = parentwindow.title

        if buttons is None:
            buttons = [_("OK")]
        assert buttons, "at least one button is required"

        assert defaultbutton is None or defaultbutton in buttons
        if defaultbutton is None and len(buttons) == 1:
            defaultbutton = buttons[0]

        return function(parentwindow, message, title, buttons, defaultbutton)

    # We can't use functools.wraps() because we want to avoid copying
    # *args showing up in help().
    result.__doc__ = doc
    result.__name__ = function.__name__
    try:
        result.__qualname__ = function.__qualname__
    except AttributeError:
        # Python 3.2.
        pass

    return result


@_messagedialog
def infodialog(*args):
    """Display a dialog with an information icon."""
    return _base.infodialog(*args)


@_messagedialog
def warningdialog(*args):
    """Display a dialog with a warning icon."""
    return _base.warningdialog(*args)


@_messagedialog
def errordialog(*args):
    """Display a dialog with an error icon."""
    return _base.errordialog(*args)


@_messagedialog
def questiondialog(*args):
    """Display a dialog with a question icon."""
    return _base.questiondialog(*args)


def colordialog(parentwindow, *, title=None, defaultcolor=color.BLACK):
    """Ask a color from the user.

    This returns the new color, or None if the user canceled the dialog.
    """
    if title is None:
        title = parentwindow.title
    return _base.colordialog(parentwindow, defaultcolor, title)


# def fontdialog(parentwindow, *, title=None, defaultfont=bananagui.Font()):
#    """Ask a font from the user.
#
#    This returns the new font, or None if the user canceled the dialog.
#    """
#    if title is None:
#        title = parentwindow.title
#    return _base.fontdialog(parentwindow, defaultfont, title)
