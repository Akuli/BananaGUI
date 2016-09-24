from gi.repository import Gtk


class WindowBase:

    def __init__(self):
        super().__init__()
        self['real_widget'].set_title(self['title'])
        self['real_widget'].connect('delete-event', self.__delete_event)

    def _bananagui_set_title(self, title):
        self['real_widget'].set_title(title)

    def _bananagui_set_resizable(self, resizable):
        self['real_widget'].set_resizable(resizable)

    def _bananagui_set_size(self, size):
        raise NotImplementedError  # TODO

    def _bananagui_set_minimum_size(self, size):
        raise NotImplementedError  # TODO

    def __delete_event(self, widget, event):
        self.destroy()
        return True  # Block GTK's delete-event handling.

    def destroy(self):
        self['real_widget'].destroy()


class Window:

    def __init__(self):
        self.raw_set('real_widget', Gtk.Window())
        super().__init__()


class ChildWindow:

    def __init__(self, parentwindow):
        self.raw_set('real_widget', Gtk.Dialog(parentwindow['real_widget']))
        super().__init__()
