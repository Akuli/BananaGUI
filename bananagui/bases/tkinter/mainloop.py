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

import bananagui.color


def reinitialize():
    global root
    root = tk.Tk()
    root.withdraw()

reinitialize()


def run():
    root.mainloop()


def quit():
    root.destroy()


def add_timeout(milliseconds, callback):
    after = root.after

    def real_callback():
        if callback() == bananagui.RUN_AGAIN:
            after(milliseconds, real_callback)

    after(milliseconds, real_callback)


def _convert_color(colorstring):
    """Convert a tkinter color string to a hexadecimal color.

    Tkinter colors are usually hexadecimal, but this function also
    handles color names like 'red' or 'SystemDefault'.
    """
    rgb = root.winfo_rgb(colorstring)
    return bananagui.color.rgb2hex(rgb, maxvalue=65535)
