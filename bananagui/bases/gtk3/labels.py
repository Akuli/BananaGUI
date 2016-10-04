from gi.repository import Gtk


class LabelBase:
    pass


class Label:

    def __init__(self, parent):
        super().__init__(parent)
        self.real_widget.raw_set(Gtk.Label())

    def _bananagui_set_text(self, text):
        self['real_widget'].set_text(text)


class ImageLabel:

    def __init__(self, parent):
        raise NotImplementedError  # TODO

    def _bananagui_set_path(self, path):
        ...
