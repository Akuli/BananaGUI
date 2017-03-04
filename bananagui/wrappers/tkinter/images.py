"""Images for the BananaGUI tkinter wrapper."""

import tkinter as tk


class Image:

    def __init__(self, real_image):
        self.real_image = real_image

    def copy(self):
        return Image(self.real_image.copy())

    @classmethod
    def from_file(cls, path, imagetype):
        self = cls(tk.PhotoImage(file=path, format=imagetype))
        size = (self.real_image.width(), self.real_image.height())
        return self, size

    @classmethod
    def from_size(cls, width, height):
        return cls(tk.PhotoImage(width=width, height=height))
