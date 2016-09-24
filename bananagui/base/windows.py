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

from bananagui import types, utils


def _check_positive_integer_pair_or_none(value):
    if value is not None:
        utils.check_positive_integer_pair(value)


# TODO: Window and Dialog classes.

class WindowBase:
    """A window baseclass.
    BananaGUI windows have a destroy() method, and it should be called
    when you don't need the window anymore. The windows can also be used
    as context managers, and the destroying will be done automatically:

        with ParentWindow() as my_window:
            ...

    The window takes a parentwindow argument on initialization. The
    parent window may be centered over the parent window, it may be
    modal or whatever the real GUI toolkit supports. It's None by
    default.

    Properties:
        parentwindow    R
            A MainWindow instance or None.
        title           RW
            The title of the window. 'Window' by default.
        resizable       RW
            True if the window can be resized, False otherwise.
        size            RWC
            Two-tuple of the width and height of the window.
            (200, 200) by default.
        minimum_size    RW
            The minimum size of the window or None.
            Like size, this is a two-tuple of width and height. The
            window cannot be resized to be smaller than this.
        destroyed       RC
            True if the widget has been destroyed, False if not.
            You can destroy a window with the destroy method or by using
            the window as a context manager.
    """
    # There is no maximum_size because X11 doesn't support it. Tkinter
    # implements it on X11, but it does that by moving the window with a
    # maximum size to the upper left corner when it's maximized.

    _bananagui_bases = ('BinBase',)
    parentwindow = types.Property('parentwindow', default=None,
                                  allow_none=True)
    title = types.Property('title', required_type=str,
                           default="BananaGUI Window")
    resizable = types.Property('resizable', required_type=bool, default=True)
    size = types.Property('size', checker=_check_positive_integer_pair_or_none,
                          default=(200, 200))
    minimum_size = types.Property('minimum_size',
                                  checker=_check_positive_integer_pair_or_none,
                                  default=None)
    destroyed = types.Property('destroyed', required_type=bool, default=False)

    def __init__(self, parentwindow=None):
        """Set the parent window."""
        super().__init__()
        self.raw_set('parentwindow', parentwindow)

    def __enter__(self):
        """Return the window."""
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Destroy the window."""
        self.destroy()

    def destroy(self):
        """Destroy the window.

        This can be called multiple times and it will do nothing after
        the first call.
        """
        if self['destroyed']:
            return
        super().destroy()
        self.raw_set('destroyed', True)


class Window:
    """A window that can have child windows.

    The window can also have a parent or it can be None. You can create
    multiple windows like this.
    """

    _bananagui_bases = ('WindowBase',)


class ChildWindow:
    """A window that has a parent window.

    """

    _bananagui_bases = ('WindowBase',)
