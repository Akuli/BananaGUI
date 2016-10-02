from gi.repository import Gtk


class LabelBase:
    pass


class Label:

    def __init__(self, parent):
        super().__init__(parent)
        self.raw_set('real_widget', Gtk.Label())

    def _bananagui_set_text(self, text):
        self['real_widget'].set_text(text)
