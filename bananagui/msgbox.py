# Copyright (c) 2016-2017 Akuli

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
try:
    import collections.abc as abcoll
except ImportError:
    import collections as abcoll

import bananagui
from bananagui import color, widgets


def _check(parentwindow, title):
    if not isinstance(parentwindow, (widgets.Window, widgets.Dialog)):
        raise TypeError("expected a Window or a Dialog, got %r"
                        % (parentwindow,))
    if title is None:
        title = parentwindow.title
    if not isinstance(title, str):
        raise TypeError("title should be a string, not %r" % (title,))
    return title


def _msgfunc(name, doc):
    """Return a new message dialog function."""
    def result(parentwindow, message, *, title=None, buttons=None,
               defaultbutton=None):
        title = _check(parentwindow, title)
        if buttons is None:
            buttons = [_("OK")]
        elif not isinstance(buttons, abcoll.Sequence):
            # Anything iterable can't be allowed because we need to for
            # loop over this multiple times and len() this.
            raise TypeError("expected a sequence, got %r" % (buttons,))

        if defaultbutton is None:
            if len(buttons) == 1:
                defaultbutton = buttons[0]
        elif defaultbutton not in buttons:
            raise ValueError("default button %r not in buttons"
                             % (defaultbutton,))
        wrapperfunc = bananagui._get_wrapper('msgbox:%s' % name)
        return wrapperfunc(parentwindow, message, title,
                           buttons, defaultbutton)

    # __qualname__ doesn't do anything on Python 3.2, but having it
    # doesn't matter.
    result.__name__ = name
    result.__qualname__ = name
    result.__doc__ = doc + """

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
    return result

info = _msgfunc('info', "Display a dialog with an information icon.")
warning = _msgfunc('warning', "Display a dialog with a warning icon.")
error = _msgfunc('error', "Display a dialog with an error icon.")
question = _msgfunc('question', "Display a dialog with a question icon.")


def colordialog(parentwindow, *, title=None, defaultcolor=color.BLACK):
    """Ask a color from the user.

    This returns the new color, or None if the user canceled the dialog.
    """
    title = _check(parentwindow, title)
    if not color._is_valid_color(defaultcolor):
        raise ValueError(
            "%r is not a valid '#RRGGBB' color, use "
            "bananagui.color to convert it" % (defaultcolor,))
    wrapperfunc = bananagui._get_wrapper('msgbox:colordialog')
    return wrapperfunc(parentwindow, defaultcolor, title)


# def fontdialog(parentwindow, *, title=None, defaultfont=bananagui.Font()):
#    """Ask a font from the user.
#
#    This returns the new font, or None if the user canceled the dialog.
#    """
#    if title is None:
#        title = parentwindow.title
#    return _wrapper.fontdialog(parentwindow, defaultfont, title)
