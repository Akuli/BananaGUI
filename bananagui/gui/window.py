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

"""Window widgets."""

from gettext import gettext as _

import bananagui
from bananagui import _base, utils
from bananagui.bases import defaults
from .containers import Bin


@utils.add_property('title')
@utils.add_property('resizable')
@utils.add_property('size', add_changed=True)
@utils.add_property('minimum_size')
@utils.add_property('showing')
class BaseWindow(_base.BaseWindow, Bin):
    """A window baseclass.

    BananaGUI windows have a close() method, and it should be called
    when you don't need the window anymore. The windows can also be used
    as context managers, and the closing will be done automatically:

        with Window() as the_window:
            ...

    There's no maximum_size attribute because X doesn't support maximum
    sizes that well. Tkinter implements a maximum size on X, but it
    does that by moving the window to the upper left corner when it's
    maximized.

    Attributes:
      title             The text in the top bar.
      resizable         True if the user can resize the window.
      size              The current window size.
                        Like most other sizes, this is a two-tuple of
                        integers.
      on_size_changed   List of callbacks that are ran when size changes.
      minimum_size      Two-tuple of smallest allowed width and height.
                        This is (None, None) by default, so the window
                        can be however big it needs to be in both
                        directions.
      showing           True if the window hasn't been hidden.
                        Hiding the window is done by setting this to
                        False and it's easier than creating a new
                        window when a window with the same content
                        needs to be displayed multiple times.
      on_close          List of callbacks that run when the user tries to
                        close the window.
                        This contains a callback that calls close() by
                        default. You can remove it or replace it with
                        something else. This doesn't run when close()
                        is called.
      closed            True if close() has been called.
    """
    # TODO: window icon?

    can_focus = True

    def __init__(self, **kwargs):
        self._title = "BananaGUI Window"
        self._resizable = True
        self._size = (200, 200)
        self._minimum_size = (None, None)
        self._showing = True
        self.on_close = [lambda w: w.close()]
        self.closed = False
        super().__init__(**kwargs)

    def _check_title(self, title):
        assert not self.closed
        assert isinstance(title, str)

    def _check_resizable(self, resizable):
        assert not self.closed
        assert isinstance(resizable, bool)

    def _check_minimum_size(self, size):
        assert not self.closed
        x, y = size
        if x is not None:
            assert isinstance(x, int)
            assert x > 0
        if y is not None:
            assert isinstance(y, int)
            assert y > 0

    def _check_size(self, size):
        assert not self.closed
        min_x, min_y = self.minimum_size
        if min_x is None:
            min_x = 1
        if min_y is None:
            min_y = 1
        x, y = size
        assert isinstance(x, int) and isinstance(y, int)
        assert x >= min_x and y >= min_y, (x, y, min_x, min_y)

    def _check_showing(self, showing):
        assert not self.closed
        assert isinstance(showing, bool)

    def close(self):
        """Close the window and set the closed attribute to True.

        This method can be called multiple times and it will do nothing
        after the first call. It's not recommended to override this, add
        a callback to the on_close list instead.
        """
        if not self.closed:
            self._close()
            self.closed = True

    def wait(self):
        """Wait until the window is closed."""
        assert not self.closed
        self._wait()

    def __enter__(self):
        return self

    def __exit__(self, *error):
        self.close()


class Window(_base.Window, BaseWindow):
    """A window that can have child windows.

    The windows don't have a parent window. You can create multiple
    windows like this.
    """


class Dialog(_base.Dialog, BaseWindow):
    """A window that has a parent window.

    This class takes a positional parentwindow argument on initialization.
    The parent window must be an instance of Window and this window may
    be centered over the parent window, it may be modal or whatever the
    real GUI toolkit supports.

    Attributes:
      parentwindow      The parent window set on initialization.
    """

    def __init__(self, parentwindow, **kwargs):
        assert isinstance(parentwindow, Window)
        self.parentwindow = parentwindow
        super().__init__(**kwargs)


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
        assert isinstance(parentwindow, Window)

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
    """Display a dialog with a question icon."""
    return _questiondialog(*args)


def colordialog(parentwindow, *, title=None, defaultcolor=bananagui.BLACK):
    """Ask a color from the user.

    This returns the new color, or None if the user canceled the dialog.
    """
    if title is None:
        title = parentwindow.title
    return _base.colordialog(parentwindow, defaultcolor, title)


def fontdialog(parentwindow, *, title=None, defaultfont=bananagui.Font()):
    """Ask a font from the user.

    This returns the new font, or None if the user canceled the dialog.
    """
    if title is None:
        title = parentwindow.title
    return _fontdialog(parentwindow, defaultfont, title)
