from gi.repository import Gtk


class BaseLabel:
    pass


class Label:

    def __init__(self, parent, **kwargs):
        self.real_widget.raw_set(Gtk.Label(justify=Gtk.Justification.CENTER))
        super().__init__(parent, **kwargs)

    def _bananagui_set_text(self, text):
        self['real_widget'].set_text(text)


class ImageLabel:

    def __init__(self, parent, **kwargs):
        raise NotImplementedError  # TODO
        super().__init__(parent, **kwargs)

    def _bananagui_set_path(self, path):
        ...
