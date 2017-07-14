from bananagui import _modules, mainloop
from bananagui._types import Callback
from .base import UpdatingProperty
from .parents import Bin


# TODO: window icon?
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

    The window size will be *default_size* before :attr:`~size` has been
    set or the user has resized the window. Note that *default_size* can
    only be given when creating a new window, it cannot be retrieved or
    changed afterwards. Use the :attr:`~size` attribute if you want to
    get or set the current size.
    """

    # There used to be a minimum_size property, but usually default_size
    # is more useful.
    #
    # If you are planning on adding a maximum_size note that X11 doesn't
    # support it that well. Tkinter implements a maximum size on X11,
    # but it does that by moving the window to the upper left corner
    # when it's maximized.

    # TODO: better docstring for title?
    title = UpdatingProperty.with_attr('_title', doc="""
    The text in the top bar.
    """)
    resizable = UpdatingProperty.with_attr('_resizable', doc="""
    True if the user can resize the window.
    """)
    hidden = UpdatingProperty.with_attr('_hidden', doc="""
    False if the window is showing normally.

    Hiding the window is easier than creating a new window when a window
    with the same content needs to be displayed multiple times.

    If you are wondering why your window isn't showing up, it's not
    necessarily hidden. There are other things that could be also wrong:

    * The window might be closed because :meth:`~close` has been called.
    * The mainloop might not be running. See :mod:`bananagui.mainloop`.
    """)

    def __init__(self, title="BananaGUI Window", child=None, *, resizable=True,
                 hidden=False, default_size=(200, 200), **bin_kwargs):
        #: A callback that runs when the user tries to close the window.
        #:
        #: This callback doesn't actually run when :meth:`~close` is
        #: called. The close method closes the window, but this runs
        #: when the *user* tries to close the window. Usually you should
        #: connect this to :func:`bananagui.mainloop.quit` or
        #: :meth:`close <close>`.
        self.on_close = Callback()

        #: A callback that runs when the window is resized by setting
        #: :attr:`~size` or by draggin the window's corners.
        #:
        #: The new width and height in pixels are passed to the
        #: connected callbacks.
        self.on_resize = Callback(int, int)

        self._title = title
        self._child = child
        self._resizable = resizable
        self._hidden = hidden
        self.__closed = False

        # a subclass like Dialog can set self.real_widget before calling
        # super().__init__(), this is not documented because this is
        # meant to be an implementation detail
        subclass_did_it = hasattr(self, 'real_widget')
        if _modules.name == 'tkinter':
            if not subclass_did_it:
                self.real_widget = _modules.tk.Toplevel()
            self.real_widget.geometry('%dx%d' % default_size)
            self.real_widget.protocol('WM_DELETE_WINDOW', self.on_close.run)
            self.real_widget.bind(
                '<Configure>',
                lambda event: self.on_resize.run(event.width, event.height))

        elif _modules.name.startswith('gtk'):
            self.__wait_loop = None       # see wait() below
            if not subclass_did_it:
                self.real_widget = _modules.Gtk.Window()

            def on_delete_event(real_widget, junk):
                self.on_close.run()
                return True     # don't let gtk close the window

            self.real_widget.set_default_size(*default_size)
            self.real_widget.connect('delete-event', on_delete_event)
            self.real_widget.connect(
                'configure-event',
                lambda window, crap: self.on_resize.run(*window.get_size()))

        else:
            raise NotImplementedError

        super().__init__(child, **bin_kwargs)

    def __repr__(self):
        if self.closed:
            return '<closed %s widget>' % self._module_and_type()
        return '<%s widget, title=%r>' % (self._module_and_type(), self.title)

    def _check_closed(self):
        if self.closed:
            raise ValueError("the window has been closed")

    # TODO: some way to run callbacks when the size changes?
    @property
    def size(self):
        """The current window size.

        Like most other sizes, this is a two-tuple of integers. Adding
        widgets to the window may change this, so setting this on
        initialization is not supported.
        """
        self._check_closed()
        if _modules.name == 'tkinter':
            widget = self.real_widget     # pep-8 line length
            return (widget.winfo_width(), widget.winfo_height())
        if _modules.name.startswith('gtk'):
            return self.real_widget.get_size()
        raise NotImplementedError

    @size.setter
    def size(self, size):
        self._check_closed()
        if _modules.name == 'tkinter':
            self.real_widget.geometry('%dx%d' % size)
        elif _modules.name.startswith('gtk'):
            self.real_widget.resize(*size)
        else:
            raise NotImplementedError
        self.render_update()

    def wait(self):
        """Wait until the window is closed."""
        self._check_closed()
        if _modules.name == 'tkinter':
            self.real_widget.wait_window()
        elif _modules.name.startswith('gtk'):
            # This is based on gtk_dialog_run in the GtkDialog C code,
            # but this is a lot shorter because this doesn't restore the
            # window to what it was before running this.
            # https://github.com/GNOME/gtk/blob/master/gtk/gtkdialog.c
            self.__wait_loop = GLib.MainLoop()
            _modules.Gdk.threads_leave()
            self.__wait_loop.run()
            _modules.Gdk.threads_enter()

    def close(self):
        """Close the window and set :attr:`~closed` to True.

        Closed windows are not displayed to the user, and most
        operations on a closed window raise an exception.

        This method can be called multiple times and it will do nothing
        after the first call.
        """
        if self.closed:
            return

        if _modules.name == 'tkinter':
            self.real_widget.destroy()
        elif _modules.name.startswith('gtk'):
            if self.__wait_loop is not None:
                self.__wait_loop.quit()
            self.real_widget.destroy()
        else:
            raise NotImplementedError

    @property
    def closed(self):
        """True if :meth:`close` has been called."""
        return self.__closed

    def add(self, child):
        self._check_closed()
        super().add(child)
        child.render(self)
        child.render_update()

        if _modules.name == 'tkinter':
            # TODO: implement expandiness properly, see comments in base.py
            #fills = {(False, False): 'none', (True, True): 'both',
            #         (True, False): 'x', (False, True): 'y'}
            #child.real_widget.pack(fill=fills[child.expand], expand=True)
            child.real_widget.pack(fill='both', expand=True)
            self.render_update()
        elif _modules.name.startswith('gtk'):
            self.real_widget.add(child.real_widget)
            child.real_widget.show()
        else:
            raise NotImplementedError

    def remove(self, child):
        self._check_closed()
        super().remove(child)
        child.unrender()    # undoes the GUI toolkit specific stuff above

    def render_update(self):
        self._check_closed()

        if _modules.name == 'tkinter':
            if self.hidden:
                self.real_widget.withdraw()
            else:
                self.real_widget.title(self.title)
                self.real_widget.resizable(self.resizable, self.resizable)
                if self.child is None:
                    self.real_widget.minsize(0, 0)
                else:
                    self.real_widget.minsize(
                        self.child.real_widget.winfo_reqwidth(),
                        self.child.real_widget.winfo_reqheight())

        elif _modules.name.startswith('gtk'):
            if self.hidden:
                self.real_widget.hide()
            else:
                self.real_widget.set_title(self.title)
                self.real_widget.set_resizable(self.resizable)
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

    def __init__(self, parentwindow, title=None, child=None, *,
                 resizable=False, **window_kwargs):
        if title is None:
            title = parentwindow.title
        self.__parentwindow = parentwindow

        if _modules.name == 'tkinter':
            self.real_widget = _modules.tk.Toplevel()
            self.real_widget.transient(parentwindow.real_widget)
        elif _modules.name.startswith('gtk'):
            self.real_widget = _modules.Gtk.Dialog(parentwindow.real_widget)

            # gtk dialogs have an action area for buttons, we don't use
            # it so let's hide it if that isn't deprecated yet...
            version = (_modules.Gtk.MAJOR_VERSION, _modules.Gtk.MINOR_VERSION)
            if version < (3, 12):
                self.real_widget.get_action_area().set_border_width(0)

            # gtk dialogs also have a separate content area, and
            # whatever is added to the dialog needs to go there
            # the content area is a Gtk.Box
            self.__content_area = self.real_widget.get_content_area()
        else:
            raise NotImplementedError

        super().__init__(title, child, resizable=resizable, **window_kwargs)

    @property
    def parentwindow(self):
        """The :class:`.Window` that this Dialog "belongs to".

        The dialog is always on top of the parent window, and it may be
        centered over it too if the underlying GUI toolkit does it by
        default.
        """
        return self.__parentwindow

    def wait(self):
        self._check_closed()
        self.real_widget.run()

    def add(self, child):
        if _modules.name.startswith('gtk'):
            # TODO: is there a nicer way to skip the parent class when
            # using super()? :D this kind of sucks
            self._check_closed()
            Bin.add(self, child)
            self.__content_area.pack_start(child.real_widget, True, True, 0)
        else:
            super().add(child)

    def remove(self, child):
        if _modules.name.startswith('gtk'):
            self._check_closed()
            Bin.remove(self, child)
            self.__content_area.remove(child.real_widget)
        else:
            super().remove(child)
