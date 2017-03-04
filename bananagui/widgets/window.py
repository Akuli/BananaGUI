from bananagui import _get_wrapper, types
from .parents import Bin


def _closecheck(window, junk=None):
    if window.closed:
        raise RuntimeError("the window has been closed")


def _sizecheck(window, size):
    if window.closed:
        raise RuntimeError("the window has been closed")
    min_x, min_y = window.minimum_size
    x, y = size
    if x < min_x or y < min_y:
        raise ValueError("size %r is smaller than minimum_size %r"
                         % (size, window.minimum_size))


@types.add_property(
    'title', type=str, extra_setter=_closecheck,
    doc="The text in the top bar.")
@types.add_property(
    'resizable', type=bool, extra_setter=_closecheck,
    doc="True if the user can resize the window.")
@types.add_property(
    'size', type=int, how_many=2, extra_setter=_sizecheck,
    add_changed=True, doc="""The current window size.

    Like most other sizes, this is a two-tuple of integers. Adding
    widgets to the window may change this, so setting this on
    initialization is not supported.
    """)
@types.add_property(
    'minimum_size', type=int, minimum=0, how_many=2,
    extra_setter=_closecheck,
    doc="""Two-tuple of smallest allowed width and height.

    If the content of the window take up more space than this, this is
    ignored. This is ``(0, 0)`` by default, so the window is always
    large enough for its content.
    """)
@types.add_property(
    'hidden', type=bool, extra_setter=_closecheck,
    doc="""False if the window is showing.

    Hiding the window is easier than creating a new window when a window
    with the same content needs to be displayed multiple times.

    If you are wondering why your window isn't showing up, it's not
    necessarily hidden. There are other things that could be also wrong:

    * The window might be closed because :meth:`~close` has been called.
    * The mainloop might not be running. See :mod:`bananagui.mainloop`.
    """)
@types.add_callback(
    'on_close',
    doc="""A callback that runs when the user tries to close the window.

    This callback doesn't actually run when :meth:`~close` is called.
    The close method closes the window, but this runs when the *user*
    tries to close the window. Usually you should connect this to
    :func:`bananagui.mainloop.quit`.
    """)
class Window(Bin):
    """A class that represents a window.

    .. code-block:: none

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

    These windows don't have a parent window. You can create multiple
    windows like this.
    """

    # There's no *maximum_size* attribute because X doesn't support
    # maximum sizes that well. Tkinter implements a maximum size on X,
    # but it does that by moving the window to the upper left corner
    # when it's maximized.

    # Most things check that the window is closed. Things that come
    # from Bin don't, but I don't think that's worth overriding
    # everything here.

    # TODO: window icon?

    can_focus = True

    def __init__(self, title="BananaGUI Window", *, child=None,
                 resizable=True, minimum_size=(0, 0), hidden=False,
                 **kwargs):
        self._prop_title = title
        self._prop_resizable = True
        self._prop_size = (200, 200)
        self._prop_minimum_size = (0, 0)
        self._prop_hidden = False
        self.__closed = False
        if not isinstance(self, Dialog):
            # Dialogs have a separate wrapper class, so we don't want to
            # add the non-Dialog wrapper here.
            wrapperclass = _get_wrapper('widgets.window:Window')
            self._wrapper = wrapperclass(self, title)
        super().__init__(child, **kwargs)
        self.resizable = resizable
        self.minimum_size = minimum_size
        self.hidden = hidden

    def close(self):
        """Close the window and set :attr:`~closed` to True.

        Closed windows are not displayed to the user, and most
        operations on a closed window raise an exception.

        This method can be called multiple times and it will do nothing
        after the first call.
        """
        if not self.closed:
            self._wrapper.close()
            self.__closed = True

    @property
    def closed(self):
        """True if :meth:`close` has been called."""
        return self.__closed

    def _repr_parts(self):
        # The title is first because it's easiest to identify the
        # window based on the title.
        parts = ['title=' + repr(self.title)] + super()._repr_parts()
        if self.closed:
            # This is the last thing and in caps because it's
            # important. Not much can be done to closed Window objects.
            parts.append('CLOSED')
        return parts

    def wait(self):
        """Wait until the window is closed."""
        _closecheck(self)
        self._wrapper.wait()


class Dialog(Window):
    """A window that has a parent window.

    .. code-block:: none

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

    This class inherits from :class:`.Window`. The title defaults to
    *parentwindow*'s title.
    """

    def __init__(self, parentwindow: Window, title=None, *,
                 resizable=False, **kwargs):
        """Initialize the dialog."""
        if title is None:
            title = parentwindow.title
        wrapperclass = _get_wrapper('widgets.window:Dialog')
        self._wrapper = wrapperclass(self, parentwindow._wrapper, title)
        self.__parentwindow = parentwindow
        super().__init__(title, resizable=resizable, **kwargs)

    @property
    def parentwindow(self):
        """The :class:`.Window` that this Dialog "belongs to".

        The dialog may be centered over the parent window, it may be
        modal or whatever the real GUI toolkit supports.
        """
        return self.__parentwindow
