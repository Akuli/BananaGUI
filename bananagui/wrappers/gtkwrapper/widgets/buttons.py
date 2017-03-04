from gi.repository import Gtk

from .basewidgets import Child


class Button(Child):

    def __init__(self, bananawidget):
        self.widget = Gtk.Button()
        self.widget.connect('clicked', self._do_click)
        super().__init__(bananawidget)

    def _do_click(self, button):
        self.bananawidget.on_click.run()

    def set_text(self, text):
        self.widget.set_label(text)

    # TODO: set_imagepath.


ImageButton = Button
