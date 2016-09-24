from gi.repository import Gtk


class EditableBase:
    pass


class Entry:

    def __init__(self, parent):
        super().__init__(parent)

        widget = Gtk.Entry()
        widget.connect('changed', self.__changed)
        self.raw_set('widget', widget)

    def __changed(self, entry):
        self.raw_set('text', entry.get_text())

    def _bananagui_set_text(self, text):
        self['real_widget'].set_text(text)

    def _bananagui_set_read_only(self, read_only):
        self['real_widget'].set_editable(not read_only)

    def select_all(self):
        self['real_widget'].select_region(0, -1)


class PlainTextView:
    # TODO: tabchar
    # TODO: In bases.py, setting the text first clears the widget and
    #       then sets the text. It should block the text.changed signal
    #       so that it's only emitted once.

    def __init__(self, parent):
        super().__init__(parent)

        widget = Gtk.TextView()
        self.__buf = widget.get_buffer()
        self.__buf.connect('changed', self.__changed)
        self.raw_set('real_widget', widget)

    def __changed(self, buf):
        self.raw_set('text', buf.get_text())

    def __get_bufiters(self):
        return self.__buf.get_start_iter(), self.__buf.get_end_iter()

    def select_all(self):
        self.__buf.select_range(*self.__get_bufiters())

    def clear(self):
        self.__buf.delete(*self.__get_bufiters())
