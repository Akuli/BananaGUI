from gi.repository import Gtk


class BaseButton:
    pass


class Button:

    def __init__(self, parent):
        super().__init__(parent)
        button = Gtk.Button()
        button.connect('clicked', self.__click)
        self.real_widget.raw_set(button)

    def __click(self, button):
        self.on_click.emit()

    def _bananagui_set_text(self, text):
        self['real_widget'].set_label(text)


class ImageButton:

    def __init__(self, parent):
        raise NotImplementedError  # TODO
