from gi.repository import Gtk


class Checkbox:

    def __init__(self, parent):
        super().__init__(parent)
        widget = Gtk.CheckButton()
        widget.connect('notify::active', self.__on_check)
        self.real_widget.raw_set(widget)

    def __on_check(self, real_widget, gparam):
        self.checked.raw_set(real_widget.get_active())

    def _bananagui_set_text(self, text):
        self['real_widget'].set_label(text)

    def _bananagui_set_checked(self, checked):
        self['real_widget'].set_active(checked)
