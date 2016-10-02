from gi.repository import Gtk


class ButtonBase:
    pass


class Button:

    def __init__(self, parent):
        super().__init__(parent)
        self.raw_set('real_widget', Gtk.Button())

    def _bananagui_set_text(self, text):
        self['real_widget'].set_label(text)
