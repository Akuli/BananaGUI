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

try:
    from collections.abc import Sequence
except ImportError:
    # Python 3.2.
    from collections import Sequence

from bananagui import _base
from bananagui.types import Property, bananadoc
from bananagui.utils import baseclass
from .containers import Bin


@baseclass
@bananadoc
class BaseWindow(_base.BaseWindow, Bin):
    """A window baseclass.

    BananaGUI windows have a destroy() method, and it should be called
    when you don't need the window anymore. The windows can also be used
    as context managers, and the destroying will be done automatically:

        with Window() as my_window:
            ...
    """
    # There is no maximum_size because X doesn't support it. Tkinter
    # implements it on X, but it does that by moving the window with a
    # maximum size to the upper left corner when it's maximized.

    resizable = Property('resizable', type=bool, default=True,
                         doc="True if the window can be resized.")
    size = Property('size', pair=True, type=int, minimum=1, default=(200, 200),
                    doc="Two-tuple of the window's current width and height.")
    minimum_size = Property(
        'minimum_size', default=None, pair=True, type=int, minimum=1,
        allow_none=True,
        doc="""Two-tuple of minimum width and height or None.

        The window cannot be resized to be smaller than this.
        """)
    showing = Property('showing', type=bool, default=True,
                       doc="True if the window is visible.")
    destroyed = Property(
        'destroyed', type=bool, default=False, settable=False,
        doc="True if the window has been destroyed.")

    def __enter__(self):
        """Return the window."""
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Call self.destroy()."""
        self.destroy()

    def wait(self):
        """Wait until the window is destroyed."""
        super().wait()

    def destroy(self):
        """Destroy the window and set self['destroyed'] to True.

        This can be called multiple times and it will do nothing after
        the first call.
        """
        if not self['destroyed']:
            super().destroy()
            self.destroyed.raw_set(True)


@bananadoc
class Window(_base.Window, BaseWindow):
    """A window that can have child windows.

    The windows don't have a parent window. You can create multiple
    windows like this.
    """

    title = Property('title', type=str, default="BananaGUI Window",
                     doc="The title of the window.")


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

    def __init__(self, parentwindow, **kwargs):
        self.parentwindow.raw_set(parentwindow)
        super().__init__(**kwargs)


def messagedialog(icon, parentwindow: Window, text: str, *,
                  title: str = None, buttons: list = None,
                  defaultbutton: str = None):
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
    assert icon in ('info', 'question', 'warning', 'error')

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
