from gi.repository import Gtk


class BaseWindow:

    def __init__(self, **kwargs):
        self['real_widget'].set_title(self['title'])
        # TODO: resizing.
        self['real_widget'].connect('delete-event', self.__delete_event)
        self['real_widget'].show()
        super().__init__(**kwargs)

    def _bananagui_set_title(self, title):
        self['real_widget'].set_title(title)

    def _bananagui_set_resizable(self, resizable):
        self['real_widget'].set_resizable(resizable)

    def _bananagui_set_size(self, size):
        self['real_widget'].resize(*size)

    def _bananagui_set_minimum_size(self, size):
        if size is None:
            size = (-1, -1)
        self['real_widget'].set_size_request(*size)

    def __delete_event(self, widget, event):
        # TODO: on_destroy signal.
        # TODO: allow the user to customize the destroying event.
        self.destroy()
        return True  # Block GTK's delete-event handling.

    def destroy(self):
        self['real_widget'].destroy()


class Window:

    def __init__(self, **kwargs):
        self.real_widget.raw_set(Gtk.Window())
        super().__init__(**kwargs)


class Dialog:

    def __init__(self, parentwindow, **kwargs):
        self.real_widget.raw_set(Gtk.Dialog(parentwindow['real_widget']))
        super().__init__(**kwargs)


def messagedialog(icon, parentwindow, text, title, buttons, defaultbutton):
    raise NotImplementedError  # TODO
