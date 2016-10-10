from gi.repository import Gtk


class Spinner:

    def __init__(self, **kwargs):
        self.real_widget.raw_set(Gtk.Spinner())
        super().__init__(**kwargs)

    def _bananagui_set_spinning(self, spinning):
        if spinning:
            self['real_widget'].start()
        else:
            self['real_widget'].stop()
