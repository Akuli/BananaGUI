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

import functools
from gettext import gettext as _

import bananagui
from bananagui import _base, utils
from bananagui.bases import defaults
from .containers import Bin


@utils.baseclass
@bananagui.bananadoc
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

    @staticmethod
    def destroy_callback(event) -> None:
        """Destroy event.widget."""
        event.widget.destroy()

    resizable = bananagui.Property(
        'resizable', type=bool, default=True,
        doc="True if the window can be resized.")
    size = bananagui.Property(
        'size', how_many=2, type=int, minimum=1, default=(200, 200),
        doc="Two-tuple of the window's current width and height.")
    minimum_size = bananagui.Property(
        'minimum_size', default=None, how_many=2, type=int, minimum=1,
        allow_none=True,
        doc="""Two-tuple of minimum width and height or None.

        The window cannot be resized to be smaller than this.
        """)
    showing = bananagui.Property(
        'showing', type=bool, default=True,
        doc="True if the window is visible.")
    on_destroy = bananagui.Signal(
        'on_destroy',
        doc="""This is emitted when the user tries to close the window.

        Unlike most other signals, this contains a callback by default.
        It's BaseWindow.destroy_callback and it destroys the window
        when it's closed. You can remove it to customize this and call
        the_window.destroy() from custom callbacks.
        """)

    def __init__(self, **kwargs):
        # TODO: this doesn't work with the class __doc__.
        self['on_destroy'].append(self.destroy_callback)
        self.__destroyed = False
        super().__init__(**kwargs)

    @property
    def destroyed(self) -> None:
        """True if the window has been destroyed.

        This is not a BananaGUI property because there's no need to
        attach callbacks to this and you can use the on_destroy signal
        instead.
        """
        return self.__destroyed

    def __enter__(self):
        """Return the window."""
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Destroy the window."""
        self.destroy()

    def wait(self) -> None:
        """Wait until the window is destroyed."""
        super().wait()

    def destroy(self) -> None:
        """Destroy the window and set self.destroyed to True.

        This method can be called multiple times and it will do nothing
        after the first call. It's not recommended to override this, use
        the on_destroy signal instead.
        """
        if not self.destroyed:
            super().destroy()
            self.__destroyed = True


@bananagui.bananadoc
class Window(_base.Window, BaseWindow):
    """A window that can have child windows.

    The windows don't have a parent window. You can create multiple
    windows like this.
    """

    title = bananagui.Property(
        'title', type=str, default="BananaGUI Window",
        doc="The title of the window.")


@bananagui.bananadoc
class Dialog(_base.Dialog, BaseWindow):
    """A window that has a parent window.

    This class takes a parentwindow argument on initialization. The
    parent window must be an instance of Window and it may be centered
    over the parent window, it may be modal or whatever the real GUI
    toolkit supports. It's None by default.
    """

    title = bananagui.Property(
        'title', type=str, default="BananaGUI Dialog",
        doc="The title of the window.")
    parentwindow = bananagui.Property(
        'parentwindow', type=Window, settable=False,
        doc="The parent window set on initialization.")

    def __init__(self, parentwindow: Window, **kwargs):
        self.parentwindow.raw_set(parentwindow)
        super().__init__(parentwindow, **kwargs)


def _messagedialog(function):
    """Return a new message dialog function."""
    # We need to modify the original function first because
    # functools.wraps overrides everything the wrapped function has.
    function.__annotations__ = {
        'parentwindow': Window, 'message': str, 'title': str,
        'buttons': utils.abc.Sequence, 'defaultbutton': str,
        'return': str,
    }
    if function.__doc__ is not None:
        # Not running with Python's optimizations.
        function.__doc__ += """

        The buttons argument should be a sequence of button texts that
        will be added to the dialog. It defaults to "OK" translated with
        gettext.gettext in a list.

        The button with `default` as its text will have keyboard focus
        by default, unless defaultbutton is None.

        The text argument is the text that will be shown in the dialog.
        If title is not given, the dialog's title will be the same as
        parentwindow's title.

        The dialog doesn't have an icon on some GUI toolkits. The text
        of the clicked button is returned, or None if the dialog is
        closed.
        """

    # TODO: does this really work? Seems like we end up with *args
    #       showing up in help().
    @functools.wraps(function)
    def result(parentwindow, message, *, title=None, buttons=None,
               defaultbutton=None) -> str:
        # TODO: add something to Widget to handle defaultbutton?
        if title is None:
            title = parentwindow['title']
        if buttons is None:
            buttons = [_("OK")]
            assert buttons, "at least one button is required"
            assert defaultbutton is None or defaultbutton in buttons
        return function(parentwindow, message, title, buttons, defaultbutton)

    return result


_infodialog = utils.find_attribute('infodialog', _base, defaults)
_warningdialog = utils.find_attribute('warningdialog', _base, defaults)
_errordialog = utils.find_attribute('errordialog', _base, defaults)
_questiondialog = utils.find_attribute('questiondialog', _base, defaults)
_fontdialog = utils.find_attribute('fontdialog', _base, defaults)


@_messagedialog
def infodialog(*args):
    """Display a dialog with an information icon."""
    return _infodialog(*args)


@_messagedialog
def warningdialog(*args):
    """Display a dialog with a warning icon."""
    return _warningdialog(*args)


@_messagedialog
def errordialog(*args):
    """Display a dialog with an error icon."""
    return _errordialog(*args)


@_messagedialog
def questiondialog(*args):
    """Display a dialog with the question icon."""
    return _questiondialog(*args)


def colordialog(parentwindow: Window, *, title: str = None,
                default: bananagui.Color = bananagui.BLACK) -> bananagui.Color:
    """Ask a color from the user.

    This returns the new color, or None if the user canceled the dialog.
    """
    if title is None:
        title = parentwindow['title']
    return _base.colordialog(parentwindow, default, title)


def fontdialog(parentwindow: Window, *, title: str = None,
               default: bananagui.Font = bananagui.Font()) -> bananagui.Font:
    """Ask a font from the user.

    This returns the new font, or None if the user canceled the dialog.
    """
    if title is None:
        title = parentwindow['title']
    return _fontdialog(parentwindow, default, title)
