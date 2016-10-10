from gi.repository import Gtk


class Spinner:

    def __init__(self, parent, **kwargs):
        # We need to hide the spinner when it's not spinning. Rest of
        # BananaGUI calls real_widget.show() when the widget is added
        # somewhere, so we need to create a container for it and add the
        # real spinner inside it.
        self.__spinner = Gtk.Spinner()
        container = Gtk.Box()
        container.pack_start(self.__spinner, True, True, 0)
        self.real_widget.raw_set(container)
        super().__init__(parent, **kwargs)

    def _bananagui_set_spinning(self, spinning):
        if spinning:
            self.__spinner.show()
            self.__spinner.start()
        else:
            self.__spinner.hide()
            self.__spinner.stop()
