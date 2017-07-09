from bananagui import _modules, mainloop
from bananagui._types import Callback
from .base import UpdatingProperty
from .parents import Bin


def _sizecheck(window, size):
    if window.closed:
        raise RuntimeError("the window has been closed")
    min_x, min_y = window.minimum_size
    x, y = size


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

    def __check_closed(self):
        if self.closed:
            raise RuntimeError("the window has been closed")

    # TODO: better docstring for title?
    title = UpdatingProperty.with_attr('_title', doc="""
    The text in the top bar.
    """)
    resizable = UpdatingProperty.with_attr('_resizable', doc="""
    True if the user can resize the window.
    """)
    minimum_size = UpdatingProperty.with_attr('_minimum_size', doc="""
    Two-tuple of smallest allowed width and height.

    This is ignored if it's too small to fit the content. By default
    this is ``(0, 0)``, so the content always fits in the window.
    """)
    hidden = UpdatingProperty.with_attr('_hidden', doc="""
    False if the window is showing.

    Hiding the window is easier than creating a new window when a window
    with the same content needs to be displayed multiple times.

    If you are wondering why your window isn't showing up, it's not
    necessarily hidden. There are other things that could be also wrong:

    * The window might be closed because :meth:`~close` has been called.
    * The mainloop might not be running. See :mod:`bananagui.mainloop`.
    """)

    # TODO: some way to run callbacks when the size changes?
    @property
    def size(self):
        """The current window size.

        Like most other sizes, this is a two-tuple of integers. Adding
        widgets to the window may change this, so setting this on
        initialization is not supported.
        """
        if _modules.name == 'tkinter':
            widget = self.real_widget     # pep-8 line length
            return (widget.winfo_width(), widget.winfo_height())
        if _modules.name == 'gtk3':
            return self.real_widget.get_size()
        raise NotImplementedError

    @size.setter
    def size(self, size):
        min_x, min_y = self.minimum_size
        x, y = size
        if x < min_x or y < min_y:
            raise ValueError("size %r is smaller than minimum_size %r"
                             % (size, window.minimum_size))

        if _modules.name == 'tkinter':
            # this runs _on_tk_configure(), that sets self._size and
            # runs render_update()
            # i know this sucks, but its not as easy as you might think
            # it is...
            self.real_widget.geometry('%dx%d' % size)
        elif _modules.name == 'gtk3':
            self.real_widget.resize(*size)
            self.render_update()
        else:
            raise 

    def __init__(self, title="BananaGUI Window", child=None, *,
                 resizable=True, minimum_size=(0, 0), hidden=False, **kwargs):
        #: A callback that runs when the user tries to close the window.
        #: 
        #: This callback doesn't actually run when :meth:`~close` is
        #: called. The close method closes the window, but this runs
        #: when the *user* tries to close the window. Usually you should
        #: connect this to :func:`bananagui.mainloop.quit`.
        self.on_close = Callback("of %s widget" % self._module_and_type())

        self._title = title
        self._child = child
        self._resizable = resizable
        self._minimum_size = minimum_size
        self._hidden = hidden
        self.__closed = False

        if _modules.name == 'tkinter':
            self.real_widget = _modules.tk.Toplevel()
            self.real_widget.bind('<Configure>', self._on_tk_configure)
            self.real_widget.protocol('WM_DELETE_WINDOW', self.on_close.run)
        elif _modules.name == 'gtk3':
            self.real_widget = _modules.Gtk.Window()
            self.real_widget.connect('configure-event', self._on_gtk_configure)
            self.real_widget.connect('delete-event', self._on_gtk_delete_event)
        else:
            raise NotImplementedError

        super().__init__(child, **kwargs)

    def __repr__(self):
        if self.closed:
            return '<closed %s widget>' % self._module_and_type()
        return '<%s widget, title=%r>' % (self._module_and_type(), self.title)

    def _on_tk_configure(self, event):
        #print("_on_tk_configure", event)
        self._size = (event.width, event.height)

        # this is ran when the content's size changes
        # tk windows can be squeezed to be too small for their content
        # by default, so we need to fix that here
        # render_update() doesn't resize the window, size's setter does
        # it instead
        self.render_update()

    def _on_gtk_configure(self, real_widget, event):
        # gtk windows seem to always be large enough to hold their
        # content, so no need to render_update()
        self._size = real_widget.get_size()

    def _on_gtk_delete_event(self, real_widget, event):
        self.on_close.run()
        return True       # don't let gtk close this window

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

    def add(self, child):
        super().add(child)
        child.render(self)
        child.render_update()

        if _modules.name == 'tkinter':
            assert child.expand == (True, True)   # lol
            child.real_widget.pack(fill='both', expand=True)
        elif _modules.name == 'gtk3':
            self.real_widget.add(child.real_widget)
            child.real_widget.show()
        else:
            raise NotImplementedError

    def remove(self, child):
        super().remove(child)
        child.unrender()    # undoes the GUI toolkit specific stuff above

    def render_update(self):
        widget = self.real_widget      # pep8 line length

        if _modules.name == 'tkinter':
            if self.hidden:
                widget.withdraw()
            else:
                minimum_size = (
                    max(self.minimum_size[0], widget.winfo_reqwidth()),
                    max(self.minimum_size[1], widget.winfo_reqheight()))
                widget.title(self.title)
                widget.resizable(self.resizable, self.resizable)
                widget.minsize(*minimum_size)

                # for some reason, deiconifying when unnecessary causes
                # weird freezing... it took a while to find this problem
                # and get this to work, so if you change this be
                # prepared to track down weird issues
                if widget.wm_state() == 'deiconified':
                    widget.deiconify()

        elif _modules.name == 'gtk3':
            if self.hidden:
                self.real_widget.hide()
            else:
                self.real_widget.resize(*self.size)
                self.real_widget.set_title(self.title)
                self.real_widget.set_resizable(self.resizable)
                self.real_widget.set_size_request(*self.minimum_size)
                self.real_widget.show()

        else:
            raise NotImplementedError


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
