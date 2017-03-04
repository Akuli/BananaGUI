import tkinter as tk

from bananagui import Align
from .basewidgets import Child, run_when_ready


anchors = {Align.LEFT: 'w',
           Align.CENTER: 'center',
           Align.RIGHT: 'e'}


class Label(Child):

    def create_widget(self, parent):
        return tk.Label(parent.widget)

    @run_when_ready
    def set_text(self, text):
        self.widget['text'] = text

    @run_when_ready
    def set_align(self, align):
        self.widget['justify'] = align.name.lower()
        self.widget['anchor'] = anchors[align]

    @run_when_ready
    def set_image(self, image):
        if image is None:
            self.widget['image'] = ''
        else:
            self.widget['image'] = image.real_image


ImageLabel = Label
