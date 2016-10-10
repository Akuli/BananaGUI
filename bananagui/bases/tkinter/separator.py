import tkinter as tk

from bananagui import HORIZONTAL, VERTICAL


class Separator:

    def __init__(self, parent, **kwargs):
        widget = tk.Frame(parent['real_widget'], border=1, relief='sunken')
        if self['orientation'] == HORIZONTAL:
            widget['height'] = 3
        if self['orientation'] == VERTICAL:
            widget['width'] = 3
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)
