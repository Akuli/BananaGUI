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

import bananagui
from bananagui import types
from .containers import Bin


def _closecheck(window, junk=None):
    if window.closed:
        raise RuntimeError("the window has been closed")


def _sizecheck(window, size):
    _closecheck(window)
    min_x, min_y = window.minimum_size
    if min_x is None:
        min_x = 1
    if min_y is None:
        min_y = 1
    x, y = size
    if x < min_x or y < min_y:
        raise ValueError("size %r is smaller than minimum_size %r"
                         % (size, window.minimum_size))


@types.add_property('title', type=str, extra_setter=_closecheck)
@types.add_property('resizable', type=bool, extra_setter=_closecheck)
@types.add_property('minimum_size', type=int, minimum=1, how_many=2,
                    allow_none=True, add_changed=True,
                    extra_setter=_closecheck)
@types.add_property('size', type=int, how_many=2, extra_setter=_sizecheck,
                    add_changed=True)
@types.add_property('hidden', type=bool, extra_setter=_closecheck)
class BaseWindow(Bin):
    """A window baseclass.

    BananaGUI windows have a close() method, and it should be called
    when you don't need the window anymore. The windows can also be used
    as context managers, and the closing will be done automatically:

        with widgets.Window("Test window") as the_window:
            ...

    There's no maximum_size attribute because X doesn't support maximum
    sizes that well. Tkinter implements a maximum size on X, but it
    does that by moving the window to the upper left corner when it's
    maximized.

    Attributes:
      title             The text in the top bar.
                        This defaults to an empty string.
      resizable         True if the user can resize the window.
      size              The current window size.
                        Like most other sizes, this is a two-tuple of
                        integers.
      on_size_changed   List of callbacks that are ran when size changes.
      minimum_size      Two-tuple of smallest allowed width and height.
                        This is (None, None) by default, so the window
                        can be however big it needs to be in both
                        directions.
      hidden            True if the window is not showing.
                        Hiding the window is easier than creating a new
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
    # Most things check that the window is closed. Things that come
    # from Bin don't, but I don't think that's worth overriding
    # everything here.

    # TODO: window icon?

    can_focus = True

    def __init__(self, title, *, resizable=True, size=(200, 200),
                 minimum_size=(None, None), hidden=False, **kwargs):
        self._title = title
        self._resizable = True
        self._size = (200, 200)
        self._minimum_size = (None, None)
        self._hidden = False
        self.on_close = [lambda w: w.close()]
        self.closed = False
        super().__init__(**kwargs)
        self.resizable = resizable
        self.size = size
        self.minimum_size = minimum_size
        self.hidden = hidden

    def _repr_parts(self):
        # The title is first because it's easiest to identify the
        # window based on the title.
        parts = ['title=' + repr(self.title)] + super()._repr_parts()
        if self.closed:
            # This is the last thing and in caps because it's
            # important. Not much can be done to closed Window objects.
            parts.append('CLOSED')
        return parts

    def close(self):
        """Close the window and set the closed attribute to True.

        This method can be called multiple times and it will do nothing
        after the first call. It's not recommended to override this, add
        a callback to the on_close list instead.
        """
        if not self.closed:
            self._base.close()
            self.closed = True

    def wait(self):
        """Wait until the window is closed."""
        _closecheck(self)
        self._base.wait()

    def __enter__(self):
        _closecheck(self)
        return self

    def __exit__(self, *error):
        self.close()


class Window(BaseWindow):
    """A window that can have child windows.

        ,---------------------------------------.
        |           Window          | _ | o | X |
        |---------------------------------------|
        |                                       |
        |                                       |
        |                                       |
        |                                       |
        |                                       |
        |                                       |
        |                                       |
        |                                       |
        |                                       |
        |                                       |
        |                                       |
        `---------------------------------------'

    The windows don't have a parent window. You can create multiple
    windows like this.
    """

    def __init__(self, title='', **kwargs):
        if not isinstance(title, str):
            raise TypeError("window title needs to be a string, not %r"
                            % (title,))
        baseclass = bananagui._get_base('widgets.window:Window')
        self._base = baseclass(self, title)
        super().__init__(title, **kwargs)


class Dialog(BaseWindow):
    """A window that has a parent window.

        ,---------------------------------------.
        |       Parent window       | _ | o | X |
        |---------------------------------------|
        |                                       |
        |                                       |
        |                                       |
        |                                       |
        |                                       |
        |                                       |
        |               ,-------------------------------.
        |               |           Dialog          | X |
        |               |-------------------------------|
        |               |                               |
        |               |                               |
        `---------------|                               |
                        |                               |
                        |                               |
                        `-------------------------------'

    This class takes a positional parentwindow argument on initialization.
    The parent window must be an instance of Window and this window may
    be centered over the parent window, it may be modal or whatever the
    real GUI toolkit supports.

    The title of a Dialog defaults to the parent window's title.

    Attributes:
      parentwindow      The parent window set on initialization.
    """

    def __init__(self, parentwindow, title=None, **kwargs):
        assert isinstance(parentwindow, Window)
        if title is None:
            title = parentwindow.title
        elif not isinstance(title, str):
            raise TypeError("Dialog title needs to be a string, not %r"
                            % (title,))
        baseclass = bananagui._get_base('widgets.window:Dialog')
        self._base = baseclass(self, parentwindow._base, title)
        self.parentwindow = parentwindow
        super().__init__(title, **kwargs)
