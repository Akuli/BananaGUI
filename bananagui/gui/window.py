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

from bananagui import _base, Property, bananadoc
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
