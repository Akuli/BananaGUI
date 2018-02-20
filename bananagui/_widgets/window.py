import functools

from bananagui import _modules
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

    def __init__(self, title="BananaGUI Window", child=None, *, resizable=True,
                 hidden=False, **kwargs):
        #: A callback that runs when the user tries to close the window.
        #:
        #: This callback doesn't actually run when :meth:`~close` is
        #: called. The close method closes the window, but this runs
        #: when the *user* tries to close the window. Usually you should
        #: connect this to :func:`bananagui.mainloop.quit` or the
        #: :meth:`close` method.
        self.on_close = Callback()

        #: A callback that runs when the window is resized by dragging
        #: the window's corners or with :meth:`resize`.
        #:
        #: The new width and height in pixels are passed to the
        #: connected callbacks.
        self.on_resize = Callback(int, int)

        self._title = title
        self._child = child
        self._resizable = resizable
        self._hidden = hidden
        self._closed = False

        # a subclass like Dialog can set self.real_widget before calling
        # super().__init__(), this is not documented because this is
        # meant to be an implementation detail
        subclass_did_it = hasattr(self, 'real_widget')
        if _modules.name == 'tkinter':
            if not subclass_did_it:
                self.real_widget = _modules.tk.Toplevel()
            self.real_widget.protocol('WM_DELETE_WINDOW', self.on_close.run)
            self.real_widget.bind(
                '<Configure>',
                lambda event: self.on_resize.run(event.width, event.height))

        elif _modules.name.startswith('gtk'):
            self._wait_loop = None       # see wait() below
            if not subclass_did_it:
                self.real_widget = _modules.Gtk.Window()

            def on_delete_event(*junk):
                self.on_close.run()
                return True     # don't let gtk close the window

            self.real_widget.connect('delete-event', on_delete_event)
            self.real_widget.connect(
                'configure-event',
                lambda window, crap: self.on_resize.run(*window.get_size()))

        else:   # pragma: no cover
            raise NotImplementedError

        super().__init__(child, **kwargs)
        self.update_everything()

    def __repr__(self):
        if self.closed:
            return '<closed %s widget, title was %r>' % (
                self._get_class_name(), self.title)

        return '<%s widget, title=%r, contains %s>' % (
            self._get_class_name(), self.title, self._content_info())

    def check_closed_decorator(func):
        @functools.wraps(func)
        def fake_func(self, *args, **kwargs):
            if self.closed:
                raise RuntimeError("the window has been closed")
            return func(self, *args, **kwargs)
        return fake_func

    # TODO: better docstring for title?
    @UpdatingProperty.updater_with_attr('_title')
    @check_closed_decorator
    def title(self):
        """The text in the top bar."""
        if _modules.name == 'tkinter':
            self.real_widget.title(self.title)
        elif _modules.name.startswith('gtk'):
            self.real_widget.set_title(self.title)
        else:   # pragma: no cover
            raise NotImplementedError

    @UpdatingProperty.updater_with_attr('_resizable')
    @check_closed_decorator
    def resizable(self):
        """True if the user can resize the window."""
        if _modules.name == 'tkinter':
            self.real_widget.resizable(self.resizable, self.resizable)
        elif _modules.name.startswith('gtk'):
            self.real_widget.set_resizable(self.resizable)
        else:   # pragma: no cover
            raise NotImplementedError

    # TODO: what if the window is minimized? check corner cases
    @UpdatingProperty.updater_with_attr('_hidden')
    @check_closed_decorator
    def hidden(self):
        """False if the window is showing normally.

        Hiding the window is easier than creating a new window when a window
        with the same content needs to be displayed multiple times.

        If you are wondering why your window isn't showing up, it's not
        necessarily hidden. There are other things that could be also wrong:

        * The window might be closed because :meth:`~close` has been called.
        * BananaGUI might not be running. See :doc:`mainloop`.
        """
        if _modules.name == 'tkinter':
            if self.hidden:
                self.real_widget.withdraw()
            else:
                self.real_widget.deiconify()
        elif _modules.name.startswith('gtk'):
            if self.hidden:
                self.real_widget.hide()
            else:
                self.real_widget.show()
        else:   # pragma: no cover
            raise NotImplementedError

    @property
    @check_closed_decorator
    def size(self):
        """The current window size.

        Like most other sizes, this is a two-tuple of integers. Setting
        this directly is not supported, use :meth:`resize` instead
        """
        if _modules.name == 'tkinter':
            widget = self.real_widget     # pep-8 line length
            return (widget.winfo_width(), widget.winfo_height())
        elif _modules.name.startswith('gtk'):
            return self.real_widget.get_size()
        else:   # pragma: no cover
            raise NotImplementedError

    # TODO: handle tkinter minsize and stuff, windows should be barely
    # enough to fit their content by default
    @check_closed_decorator
    def resize(self, new_width, new_height):
        """Try to change :attr:`size`.

        Usually calling this method changes the size, but there are no
        guarantees that the size actually changes in BananaGUI. GUI
        toolkits can only ask the window manager nicely if it would like
        to change the window size, and that's what this method does.

        .. note::
            Adding more widgets to the window may change the size, so
            it's best to call this method after creating the widgets.
        """
        if _modules.name == 'tkinter':
            self.real_widget.geometry('%dx%d' % (new_width, new_height))
        elif _modules.name.startswith('gtk'):
            self.real_widget.resize(new_width, new_height)
        else:   # pragma: no cover
            raise NotImplementedError

    @check_closed_decorator
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
            self._wait_loop = _modules.GLib.MainLoop()
            _modules.Gdk.threads_leave()
            self._wait_loop.run()
            _modules.Gdk.threads_enter()
        else:   # pragma: no cover
            raise NotImplementedError

    @property
    def closed(self):
        """True if :meth:`close` has been called."""
        return self._closed

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
            if self._wait_loop is not None:
                self._wait_loop.quit()
            self.real_widget.destroy()
        else:   # pragma: no cover
            raise NotImplementedError
        self._closed = True

    del check_closed_decorator


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

    _this_is_a_dialog = True    # for Bin in parents.py

    def __init__(self, parentwindow, title=None, child=None, *,
                 resizable=False, **window_kwargs):
        if title is None:
            title = parentwindow.title
        self._parentwindow = parentwindow

        if _modules.name == 'tkinter':
            self.real_widget = _modules.tk.Toplevel()
            self.real_widget.transient(parentwindow.real_widget)
        elif _modules.name.startswith('gtk'):
            self.real_widget = _modules.Gtk.Dialog(parentwindow.real_widget)

            # gtk dialogs have an action area for buttons, we don't use
            # it so let's hide it using the deprecated get_action_area()
            try:
                self.real_widget.get_action_area().set_border_width(0)
            except AttributeError:
                pass

            # gtk dialogs also have a separate content area, and
            # whatever is added to the dialog needs to go there
            # the content area is a Gtk.Box
            self._content_area = self.real_widget.get_content_area()
        else:   # pragma: no cover
            raise NotImplementedError

        super().__init__(title, child, resizable=resizable, **window_kwargs)

    @property
    def parentwindow(self):
        """The :class:`.Window` that this Dialog "belongs to".

        The dialog is always on top of the parent window, and it may be
        centered over it too if the underlying GUI toolkit does it by
        default.
        """
        return self._parentwindow

    def wait(self):
        if _modules.name.startswith('gtk'):
            self._check_closed()
            self.real_widget.run()
        else:
            super().wait()

    def add(self, child):
        super().add(child)
        if _modules.name.startswith('gtk'):
            self._content_area.pack_start(child.real_widget, True, True, 0)

    def remove(self, child):
        if _modules.name.startswith('gtk'):
            self._check_closed()
            Bin.remove(self, child)
            self._content_area.remove(child.real_widget)
        else:
            super().remove(child)
