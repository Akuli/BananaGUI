from gi.repository import Gtk


class TextBase:
    pass


class Entry:

    def __init__(self, parent):
        super().__init__(parent)

        widget = Gtk.Entry()
        widget.connect('changed', self.__changed)
        self.real_widget.raw_set(widget)

    def __changed(self, entry):
        self.text.raw_set(entry.get_text())

    def _bananagui_set_text(self, text):
        self['real_widget'].set_text(text)

    def _bananagui_set_read_only(self, read_only):
        self['real_widget'].set_editable(not read_only)

    def select_all(self):
        self['real_widget'].select_region(0, -1)


class PlainTextView:
    # TODO: tabchar

    def __init__(self, parent):
        super().__init__(parent)
        widget = Gtk.TextView()
        self.__buf = widget.get_buffer()
        self.__buf.connect('changed', self.__changed)
        self.real_widget.raw_set(widget)

    def __changed(self, buf):
        self.text.raw_set(buf.get_text())

    def __bounds(self):
        return self.__buf.get_start_iter(), self.__buf.get_end_iter()

    def select_all(self):
        self.__buf.select_range(*self.__bounds())

    def clear(self):
        self.__buf.delete(*self.__bounds())

    def append_text(self):
        raise NotImplementedError("TODO")