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

"""Handy dialog functions.

All public functions in this module take these arguments:

- *parentwindow:* A bananagui.widgets.Window object. Usually the dialog
  will be centered on this window.
- *title:* The title of the dialog, defaults to the parentwindow's
  title.

The info(), warning(), error() and question() functions also take these
arguments:

- *buttons:* This should be an iterable of button texts that will be
  added to the dialog. BananaGUI needs to iterate over this multiple
  times, so I don't recommend using an iterator for this.
- *defaultbutton:* This should be a string in *buttons*. The default
  button will have keyboard focus by default.
- *text:* This is the text that will be shown in the dialog.
- *title:* The title of the dialog, defaults to the parentwindow's title.

Most functions return whatever the user chooses or None if the dialog is
closed. For example, info(), warning(), error() and question() return
the text of the clicked button or None.
"""

from gettext import gettext as _
try:
    import collections.abc as abcoll
except ImportError:
    import collections as abcoll

import bananagui
from bananagui import color, widgets

__all__ = ['info', 'warning', 'error', 'question', 'colordialog']


def _message(icon, parentwindow, msg, title, buttons, defaultbutton):
    if title is None:
        title = parentwindow.title
    if defaultbutton is not None and defaultbutton not in buttons:
        raise ValueError("default button %r not in buttons"
                         % (defaultbutton,))
    # The wrapper functions can't import the MessageKind enum from this
    # module, so they get the name of tne enum member instead.
    wrapperfunc = bananagui._get_wrapper('msgbox:message')
    return wrapperfunc(icon, parentwindow, msg, title, buttons,
                       defaultbutton)


def info(parentwindow: widgets.Window, message: str, buttons, *,
         title: str = None, defaultbutton: str = None):
    """Display an info message."""
    return _message('info', parentwindow, message, title, buttons,
                    defaultbutton)


def warning(parentwindow: widgets.Window, message: str, buttons, *,
            title: str = None, defaultbutton: str = None):
    """Display a warning message."""
    return _message('warning', parentwindow, message, title, buttons,
                    defaultbutton)


def error(parentwindow: widgets.Window, message: str, buttons, *,
          title: str = None, defaultbutton: str = None):
    """Display an error message."""
    return _message('error', parentwindow, message, title, buttons,
                    defaultbutton)


def question(parentwindow: widgets.Window, message: str, buttons, *,
             title: str = None, defaultbutton: str = None):
    """Display a question message."""
    return _message('question', parentwindow, message, title, buttons,
                    defaultbutton)


def colordialog(parentwindow: widgets.Window, *, title: str = None,
                defaultcolor: str = color.BLACK):
    """Ask a color from the user.

    This returns the new color, or None if the user canceled the dialog.
    """
    if title is None:
        title = parentwindow.title
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
