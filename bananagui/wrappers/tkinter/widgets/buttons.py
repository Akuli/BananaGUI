import tkinter as tk

from .basewidgets import Child, run_when_ready


class Button(Child):

    def create_widget(self, parent):
        widget = tk.Button(parent.widget, command=self._do_click)
        widget.bind('<Return>', self._do_click)
        return widget

    def _do_click(self, event=None):
        self.bananawidget.on_click.run()

    @run_when_ready
    def set_text(self, text):
        self.widget['text'] = text

    @run_when_ready
    def set_image(self, image):
        if image is None:
            self.widget['image'] = ''
        else:
            self.widget['image'] = image.real_image


ImageButton = Button
