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

from tkinter import ttk

from .basewidgets import Child, run_when_ready


class Progressbar(Child):

    def create_widget(self, parent):
        return ttk.Progressbar(parent.widget)

    @run_when_ready
    def set_bouncing(self, bouncing):
        if bouncing:
            self.widget['mode'] = 'indeterminate'
            self.widget.start(20)  # Move every 20 milliseconds.
        else:
            # Unfortunately there's no better way to hide the moving
            # part of the bar when we don't want it to bounce.
            self.widget['mode'] = 'determinate'
            self.widget.stop()

    @run_when_ready
    def set_progress(self, progress):
        self.widget.stop()  # Reset it.
        step = progress * 100
        if step > 99.99:
            # The widget would go back to zero if we stepped it this
            # much.
            step = 99.99
        self.widget.step(step)


BouncingProgressbar = Progressbar
