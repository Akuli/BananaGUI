from gi.repository import Gtk

from .basewidgets import Child


class Entry(Child):

    def __init__(self, bananawidget):
        self.widget = Gtk.Entry()
        self.widget.connect('changed', self._do_changed)
        super().__init__(bananawidget)

    def _do_changed(self, entry):
        self.bananawidget.text = entry.get_text()

    def set_text(self, text):
        self.widget.set_text(text)

    def set_grayed_out(self, grayed_out):
        self.widget.set_editable(not grayed_out)
        super().set_grayed_out(grayed_out)

    def set_secret(self, secret):
        self.widget.set_visibility(not secret)

    def select_all(self):
        self.widget.select_region(0, -1)


class TextEdit(Child):
    # TODO: tabchar

    def __init__(self, bananawidget):
        self.widget = Gtk.TextView()
        self._textbuf = self.widget.get_buffer()
        self._changed_id = self._textbuf.connect('changed', self._do_changed)
        self._setting_text = False
        super().__init__(bananawidget)

    def _do_changed(self, buf):
        self._setting_text = True
        self.text = buf.get_text(buf.get_start_iter(),
                                 buf.get_end_iter(), True)
        self._setting_text = False

    def select_all(self):
        self._textbuf.select_range(self._textbuf.get_start_iter(),
                                   self._textbuf.get_end_iter())

    def set_text(self, text):
        # We get weird warnings if we remove this check.
        if not self._setting_text:
            # set_text() first clears the buffer and then inserts to
            # it, but we must not run the callback twice.
            with self._textbuf.handler_block(self._changed_id):
                self._textbuf.set_text(text)
