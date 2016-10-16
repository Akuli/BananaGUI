# Copyright (c) 2016 Akuli

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import tkinter as tk
from tkinter import font

import bananagui
from . import mainloop


class Checkbox:

    def __init__(self, parent, **kwargs):
        self.__var = tk.IntVar()
        self.__var.trace('w', self.__var_changed)

        widget = tk.Checkbutton(parent['real_widget'], variable=self.__var)

        # The checkboxes have white foreground on a white background by
        # default with my dark GTK+ theme.
        box_bg = mainloop.convert_color(widget['selectcolor'])
        checkmark = mainloop.convert_color(widget['fg'])
        if box_bg.brightness < 0.5 and checkmark.brightness < 0.5:
            # Make the background of the actual box where the checkmark
            # goes white, and leave the checkmark dark.
            widget['selectcolor'] = '#ffffff'
        if box_bg.brightness >= 0.5 and checkmark.brightness >= 0.5:
            # Make the background black and leave the checkmark light.
            # This runs with my GTK+ theme.
            widget['selectcolor'] = '#000000'

        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def __var_changed(self, name, empty_string, mode):
        self.checked.raw_set(bool(self.__var.get()))

    def _bananagui_set_text(self, text):
        self['real_widget']['text'] = text

    def _bananagui_set_checked(self, checked):
        self.__var.set(1 if checked else 0)


class Dummy:

    def __init__(self, parent, **kwargs):
        self.real_widget.raw_set(tk.Frame(parent['real_widget']))
        super().__init__(parent, **kwargs)


class Separator:

    def __init__(self, parent, **kwargs):
        widget = tk.Frame(parent['real_widget'], border=1, relief='sunken')
        if self['orientation'] == bananagui.HORIZONTAL:
            widget['height'] = 3
        if self['orientation'] == bananagui.VERTICAL:
            widget['width'] = 3
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)


def _select_all(event):
    try:
        # Tkinter's spinboxes don't have a selection_range method for
        # some reason, but entries have it.
        event.widget.selection('range', 0, 'end')
    except tk.TclError:
        # Maybe selection_range doesn't work with spinboxes on old Tk
        # versions?
        pass


class Spinbox:

    def __init__(self, parent, **kwargs):
        self.__var = tk.StringVar()
        self.__var.trace('w', self.__var_changed)

        widget = tk.Spinbox(
            parent['real_widget'], textvariable=self.__var,
            values=tuple(self._bananagui_ranged_valuerange))
        widget.bind('<Control-A>', _select_all)
        widget.bind('<Control-a>', _select_all)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def __var_changed(self, tkname, empty_string, mode):
        try:
            value = int(self.__var.get())
            if value not in self._bananagui_ranged_valuerange:
                return
        except ValueError:
            return
        self.value.raw_set(value)

    def _bananagui_set_value(self, value):
        # This tells tkinter to call self.__var_changed.
        self.__var.set(str(value))


_tkinter_orients = {
    bananagui.HORIZONTAL: 'horizontal',
    bananagui.VERTICAL: 'vertical',
}


class Slider:

    def __init__(self, parent, **kwargs):
        # I think tkinter's scales are upside down when the orientation
        # is vertical because the bigger number is at the bottom.
        # Unfortunately this can't be fixed by setting resolution to a
        # negative value :(
        widget = tk.Scale(parent['real_widget'], from_=self['minimum'],
                          to=self['maximum'], resolution=self['step'],
                          orient=_tkinter_orients[self['orientation']])
        # There's no value changed thing, but all tkinter widgets have
        # a ButtonRelease signal that's emitted when the left mouse key
        # is lifted. It seems to me that sliders can't be controlled
        # with the keyboard so this seems to work.
        widget.bind('<ButtonRelease>', self.__value_changed)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def __value_changed(self, event):
        self.value.raw_set(event.widget.get())

    def _bananagui_set_value(self, value):
        self['real_widget'].set(value)


def get_font_families():
    return font.families()
