from gi.repository import Gtk


class BaseWindow:

    def __init__(self, **kwargs):
        window = self['real_widget']
        window.set_title(self['title'])
        window.connect('delete-event', self.__delete_event)
        window.show()
        super().__init__(**kwargs)

    def _bananagui_set_title(self, title):
        self['real_widget'].set_title(title)

    # TODO: resizable and size don't work correctly if resizable is
    # False but size is set.
    def _bananagui_set_resizable(self, resizable):
        self['real_widget'].set_resizable(resizable)

    def _bananagui_set_size(self, size):
        self['real_widget'].resize(*size)

    def _bananagui_set_minimum_size(self, size):
        if size is None:
            size = (-1, -1)
        self['real_widget'].set_size_request(*size)

    def __delete_event(self, widget, event):
        self.on_destroy.emit()
        return True  # Block GTK's delete-event handling.

    def wait(self):
        raise NotImplementedError  # TODO

    def destroy(self):
        self['real_widget'].destroy()


class Window:

    def __init__(self, **kwargs):
        self.real_widget.raw_set(Gtk.Window())
        super().__init__(**kwargs)
