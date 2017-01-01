# Copyright (c) 2016-2017 Akuli

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

import bananagui
from .basewidgets import Child, run_when_ready


anchors = {bananagui.LEFT: 'w',
           bananagui.CENTER: 'center',
           bananagui.RIGHT: 'e'}


class Label(Child):

    def create_widget(self, parent):
        return tk.Label(parent.real_widget)

    @run_when_ready
    def set_text(self, text):
        self.real_widget['text'] = text

    @run_when_ready
    def set_align(self, align):
        self.real_widget['justify'] = align.name.lower()
        self.real_widget['anchor'] = anchors[align]

    @run_when_ready
    def set_image(self, image):
        if image is None:
            self.real_widget['image'] = ''
        else:
            self.real_widget['image'] = image.real_image


ImageLabel = Label
