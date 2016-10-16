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

import bananagui
from bananagui import utils
from . import containers


def _destroy_callback(event):
    """Destroy event.widget."""
    event.widget.destroy()


@utils.baseclass
@bananagui.bananadoc
class BaseWindow(bananagui._base.BaseWindow, containers.Bin):
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
        It calls self.destroy and you can remove it if you don't want
        the window to get destroyed when the user tries to close it. You
        can also call self.destroy() from other callbacks.
        """)

    def __init__(self, **kwargs):
        self['on_destroy'].append(_destroy_callback)
        self.__destroyed = False
        super().__init__(**kwargs)

    @property
    def destroyed(self):
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

    def wait(self):
        """Wait until the window is destroyed."""
        super().wait()

    def destroy(self):
        """Destroy the window and set self.destroyed to True.

        This method can be called multiple times and it will do nothing
        after the first call. It's not recommended to override this, use
        the on_destroy signal instead.
        """
        if not self.destroyed:
            super().destroy()
            self.__destroyed = True


@bananagui.bananadoc
class Window(bananagui._base.Window, BaseWindow):
    """A window that can have child windows.

    The windows don't have a parent window. You can create multiple
    windows like this.
    """

    title = bananagui.Property(
        'title', type=str, default="BananaGUI Window",
        doc="The title of the window.")
