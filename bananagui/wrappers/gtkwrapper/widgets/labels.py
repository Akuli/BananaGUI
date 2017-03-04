from gi.repository import Gtk

from bananagui import Align
from .basewidgets import Child


haligns_and_justifys = {
    Align.LEFT: (Gtk.Align.START, Gtk.Justification.LEFT),
    Align.CENTER: (Gtk.Align.CENTER, Gtk.Justification.FILL),
    Align.RIGHT: (Gtk.Align.END, Gtk.Justification.RIGHT),
}


class Label(Child):

    def __init__(self, bananawidget):
        self.widget = Gtk.Label(justify=Gtk.Justification.CENTER)
        super().__init__(bananawidget)

    def set_text(self, text):
        self.widget.set_text(text)

    def set_align(self, align):
        halign, justify = haligns_and_justifys[align]
        self.widget.set_halign(halign)
        self.widget.set_justify(justify)

    # TODO: implement set_image.
