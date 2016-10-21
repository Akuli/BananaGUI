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

import bananagui
from . import containers


class _TooltipBase:
    """Tooltips for tkinter.

    License notice: This class has nothing to do with idlelib.ToolTip. I
    didn't copy-paste this from idlelib and I didn't read idlelib's
    tooltip.py when I wrote this. I wrote my own tooltip manager mainly
    because I didn't have the time to find out how I'm allowed to use
    idlelib's code.
    """

    # This should never contain more than one window at a time, but we
    # allow multiple windows to make sure nothing breaks if we have
    # multiple tipwindows at the same time for some reason.
    __tipwindows = set()

    def __init__(self, *args, **kwargs):
        self.__got_mouse = False
        self['real_widget'].bind('<Enter>', self.__enter)
        self['real_widget'].bind('<Leave>', self.__leave)
        self['real_widget'].bind('<Motion>', self.__motion)
        super().__init__(*args, **kwargs)

    def __destroy_tipwindows(self, event=None):
        while self.__tipwindows:
            tipwindow = self.__tipwindows.pop()
            tipwindow.destroy()

    def __enter(self, event):
        if event.widget is not self['real_widget']:
            # For some reason, toplevels get also notified of their
            # childrens' events.
            return
        self.__destroy_tipwindows()
        self.__got_mouse = True
        event.widget.after(1000, self.__show)

    def __leave(self, event):
        if event.widget is not self['real_widget']:
            return
        self.__destroy_tipwindows()
        self.__got_mouse = False

    def __motion(self, event):
        self.__mousex = event.x_root
        self.__mousey = event.y_root

    def __show(self):
        if not self.__got_mouse:
            return
        self.__destroy_tipwindows()
        if self['tooltip'] is not None:
            tipwindow = tk.Toplevel()
            tipwindow.geometry('+%d+%d' % (self.__mousex+10, self.__mousey-10))
            tipwindow.bind('<Motion>', self.__destroy_tipwindows)
            tipwindow.overrideredirect(True)
            self.__tipwindows.add(tipwindow)

            # If you modify this, make sure to always define either no
            # colors at all or both foreground and background. Otherwise
            # the label will have light text on a light background or
            # dark text on a dark background on some systems.
            label = tk.Label(tipwindow, text=self['tooltip'],
                             fg='black', bg='white')
            label.pack()

    def _bananagui_set_tooltip(self, tooltip):
        # This needs to be defined, but it doesn't need to do anything
        # because the new tooltip is avaliable as self['tooltip'].
        pass


class Widget:
    pass


class Parent:
    pass


_tkinter_fills = {
    (True, True): 'both',
    (True, False): 'x',
    (False, True): 'y',
    (False, False): 'none',
}
_expand_indexes = {
    bananagui.HORIZONTAL: 0,
    bananagui.VERTICAL: 1,
}


class Child(_TooltipBase):

    def __init__(self, **kwargs):
        self._bananagui_tkinter_packed = False  # See also layouts.py.
        super().__init__(**kwargs)

    def _bananagui_set_expand(self, expand):
        if self._bananagui_tkinter_packed:
            # Update the pack expanding. By having this here we can make
            # sure that the pack options are changed when the expand is
            # changed.
            pack_kwargs = {'fill': _tkinter_fills[expand]}
            if isinstance(self['parent'], containers.Box):
                index = _expand_indexes[self['parent']['orientation']]
                pack_kwargs['expand'] = expand[index]
            else:
                # It's not a box. We need a default value.
                pack_kwargs['expand'] = (expand == (True, True))
            self['real_widget'].pack(**pack_kwargs)

    def _bananagui_set_grayed_out(self, grayed_out):
        self['real_widget']['state'] = 'disable' if grayed_out else 'normal'
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

"""Button widgets."""

import tkinter as tk


class BaseButton:

    def __init__(self, parent, **kwargs):
        widget = tk.Button(parent['real_widget'], command=self.on_click.emit)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)


class Button:

    def _bananagui_set_text(self, text):
        self['real_widget'].config(text=text)


class ImageButton:

    def __init__(self, parent, **kwargs):
        # This is needed to avoid garbage collection.
        self.__image = None
        super().__init__(parent, **kwargs)

    def _bananagui_set_imagepath(self, path):
        if path is None:
            self['real_widget']['image'] = ''
            self.__image = None
        else:
            self.__image = tk.PhotoImage(file=path)
            self['real_widget']['image'] = self.__image
import itertools
import tkinter as tk


class Canvas:

    def __init__(self, parent, **kwargs):
        width, height = self['size']
        widget = tk.Canvas(parent['real_widget'], bg=self['background'].hex,
                           width=width, height=height)
        widget.bind('<Configure>', self.__configure)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def __configure(self, event):
        self.size.raw_set((event.width, event.height))

    def _bananagui_set_minimum_size(self, size):
        width, height = size
        self['real_widget'].config(width=width, height=height)

    def _bananagui_set_background(self, background):
        self['real_widget'].config(bg=background.hex)

    def draw_line(self, start, end, thickness, color):
        self['real_widget'].create_line(
            # *start, *end doesn't work on Pythons older than 3.5.
            *itertools.chain(start, end),
            fill=color.hex, width=thickness)

    def draw_polygon(self, *corners, fillcolor, linecolor, linethickness):
        kwargs = {}
        if fillcolor is not None:
            kwargs['fill'] = fillcolor.hex
        if linecolor is not None:
            kwargs['outline'] = linecolor.hex
        self['real_widget'].create_polygon(
            *itertools.chain.from_iterable(corners),
            width=linethickness, **kwargs)

    def draw_oval(self, center, xradius, yradius, fillcolor,
                  linecolor, linethickness):
        centerx, centery = center
        kwargs = {}
        if fillcolor is not None:
            kwargs['fill'] = fillcolor.hex
        if linecolor is not None:
            kwargs['outline'] = linecolor.hex
        self['real_widget'].create_oval(
            centerx - xradius, centery - yradius,
            centerx + xradius, centery + yradius,
            width=linethickness, **kwargs)
import tkinter as tk

from . import mainloop


def set_clipboard_text(text):
    mainloop.root.clipboard_clear()
    mainloop.root.clipboard_append(text)


def get_clipboard_text():
    try:
        return mainloop.root.clipboard_get()
    except tk.TclError:
        # There's nothing on the clipboard.
        return ''
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

import bananagui


class Bin:

    def _bananagui_set_child(self, child):
        if self['child'] is not None:
            self['child']['real_widget'].pack_forget()
            self['child']._bananagui_tkinter_packed = False
        if child is not None:
            child['real_widget'].pack()
            child._bananagui_tkinter_packed = True
            child._bananagui_set_expand(child['expand'])  # See bases.py.


_tkinter_fills = {
    # child['expand']: fill
    (True, True): 'both',
    (True, False): 'x',
    (False, True): 'y',
    (False, False): 'none',
}
_appendsides = {
    # Appending to a box adds a child to the beginning of the box, and
    # then the next child towards the center from the first child and
    # so on.
    bananagui.HORIZONTAL: 'left',
    bananagui.VERTICAL: 'top',
}


class Box:

    def __init__(self, parent, **kwargs):
        self.real_widget.raw_set(tk.Frame(parent['real_widget']))
        super().__init__(parent, **kwargs)

    def _bananagui_box_append(self, child):
        child['real_widget'].pack(
            side=_appendsides[self['orientation']],
            fill=_tkinter_fills[child['expand']],
        )
        child._bananagui_tkinter_packed = True

        # Set the pack expanding, see ChildBase._bananagui_set_expand
        # in bases.py.
        child._bananagui_set_expand(child['expand'])

    def _bananagui_box_remove(self, child):
        child['real_widget'].pack_forget()
        child._bananagui_tkinter_packed = False
import tkinter as tk
from tkinter import colorchooser

from . import mainloop


class Dialog:

    def __init__(self, parentwindow, **kwargs):
        widget = tk.Toplevel(parentwindow['real_widget'])
        self.real_widget.raw_set(widget)
        super().__init__(**kwargs)


def colordialog(parentwindow, color, title):
    result = colorchooser.askcolor(
        color.hex, title=title,
        parent=parentwindow['real_widget'])
    if result == (None, None):
        return None
    return mainloop.convert_color(result[1])
"""BananaGUI tkinter base."""

# flake8: noqa

from .bases import Widget, Parent, Child
from .buttons import BaseButton, Button, ImageButton
from .canvas import Canvas
from .clipboard import set_clipboard_text, get_clipboard_text
from .containers import Bin, Box
from .dialogs import Dialog, colordialog
from .labels import BaseLabel, Label, ImageLabel
from .mainloop import init, main, quit
from .misc import (Checkbox, Dummy, Separator, Spinbox, Slider,
                   Progressbar, get_font_families)
from .textwidgets import TextBase, Entry, PlainTextView
from .timeouts import add_timeout
from .trayicon import TrayIcon
from .window import BaseWindow, Window
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

"""Labels for the BananaGUI tkinter wrapper."""

import tkinter as tk


class BaseLabel:

    def __init__(self, parent, **kwargs):
        self.real_widget.raw_set(tk.Label(parent['real_widget']))
        super().__init__(parent, **kwargs)


class Label:

    def _bananagui_set_text(self, text):
        self['real_widget']['text'] = text


class ImageLabel:

    def __init__(self, parent, **kwargs):
        self.__photoimage = None
        super().__init__(parent, **kwargs)

    def _bananagui_set_path(self, path):
        if path is None:
            # Remove the old image if any.
            self['real_widget']['image'] = ''
            self.__photoimage = None
        else:
            # Tkinter needs a reference to the PhotoImage.
            self.__photoimage = tk.PhotoImage(file=path)
            self['real_widget']['image'] = self.__photoimage
import tkinter as tk

import bananagui


root = None


def init():
    global root
    root = tk.Tk()
    root.withdraw()


def main():
    root.mainloop()


def quit():
    global root
    root.destroy()
    root = None


def convert_color(colorstring):
    """Convert a tkinter color string to a BananaGUI color.

    Unlike bananagui.Color.from_hex, this also handles color names like
    'red'.
    """
    # I have no idea why the biggest value is 65535. To scale it down to
    # 255 we need to divide it by 65535/255=257.
    rgb = [value // 257 for value in root.winfo_rgb(colorstring)]
    return bananagui.Color(*rgb)
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
from tkinter import font, ttk

import bananagui
from bananagui import utils
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
            # Tkinter doesn't know how to handle ranges.
            values=tuple(self['valuerange']))
        widget.bind('<Control-A>', _select_all)
        widget.bind('<Control-a>', _select_all)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def __var_changed(self, tkname, empty_string, mode):
        try:
            value = int(self.__var.get())
            if value not in self['valuerange']:
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
        minimum = min(self['valuerange'])
        maximum = max(self['valuerange'])
        step = utils.rangestep(self['valuerange'])
        widget = tk.Scale(parent['real_widget'], from_=minimum,
                          to=maximum, resolution=step,
                          orient=_tkinter_orients[self['orientation']])

        # There seems to be no way to change a Scale's value with the
        # keyboard so this seems to work.
        # http://stackoverflow.com/a/16970862
        widget.bind('<ButtonRelease>', self.__value_changed)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def __value_changed(self, event):
        self.value.raw_set(event.widget.get())

    def _bananagui_set_value(self, value):
        self['real_widget'].set(value)


class Progressbar:

    def __init__(self, parent, **kwargs):
        widget = ttk.Progressbar(
            parent['real_widget'],
            orient=_tkinter_orients[self['orientation']])
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def _bananagui_set_progress(self, progress):
        self['real_widget'].stop()  # Reset it.
        step = progress * 100
        if step >= 99.99:
            # The widget would go back to zero if we stepped it this
            # much.
            step = 99.99
        self['real_widget'].step(step)


def get_font_families():
    return font.families()
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


class TextBase:

    def __init__(self, parent, **kwargs):
        self['real_widget'].bind('<Control-A>', self.__select_all)
        self['real_widget'].bind('<Control-a>', self.__select_all)
        super().__init__(parent, **kwargs)

    def __select_all(self, event):
        self.select_all()
        return 'break'


class Entry:

    def __init__(self, parent, **kwargs):
        self.__var = tk.StringVar()
        self.__var.trace('w', self.__var_changed)
        widget = tk.Entry(parent['real_widget'], textvariable=self.__var)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def __var_changed(self, tkname, empty_string, mode):
        self.text.raw_set(self.__var.get())

    def _bananagui_set_text(self, text):
        self.__var.set(text)

    def _bananagui_set_read_only(self, read_only):
        state = 'readonly' if read_only else 'normal'
        self['real_widget']['state'] = state

    def select_all(self):
        self['real_widget'].selection_range(0, 'end')
        self['real_widget'].focus()


class PlainTextView:

    def __init__(self, parent, **kwargs):
        # TODO: Add more keyboard shortcuts.
        # A larger width or height would prevent the widget from
        # shrinking when needed.
        widget = tk.Text(parent['real_widget'], width=1, height=1)
        widget.bind('<<Modified>>', self.__edit_modified)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def select_all(self):
        """Select all text in the widget."""
        # The end-1c doesn't get what tkinter thinks of as the last
        # character, which is a newline.
        self['real_widget'].tag_add('sel', 0.0, 'end-1c')
        self['real_widget'].focus()

    def __edit_modified(self, event):
        """Update the widget's text property."""
        self.text.raw_set(event.widget.get(0.0, 'end-1c'))

        # This function will be called twice if the event is not unbound
        # first.
        event.widget.unbind('<<Modified>>')

        # Tell tkinter that the text in the widget has not been
        # modified. This will run again when the text is modified.
        event.widget.edit_modified(False)

        # Bind again.
        event.widget.bind('<<Modified>>', self.__edit_modified)

    def clear(self):
        self['real_widget'].delete(0.0, 'end')

    def append_text(self, text):
        self['real_widget'].insert('end', text)

    # Unfortunately read_only and grayed_out need to be done the same
    # way.
    def __set_disable(self, disable):
        self['real_widget']['state'] = 'disable' if disable else 'normal'

    def _bananagui_set_read_only(self, read_only):
        self.__set_disable(read_only or self['grayed_out'])

    def _bananagui_set_grayed_out(self, grayed_out):
        self.__set_disable(self['read_only'] or grayed_out)
import bananagui
from . import mainloop


def add_timeout(milliseconds, callback):
    after = mainloop.root.after

    def real_callback():
        if callback() == bananagui.RUN_AGAIN:
            after(milliseconds, real_callback)

    after(milliseconds, real_callback)
import warnings


class TrayIcon:

    def __init__(self, iconpath, **kwargs):
        warnings.warn("Tkinter doesn't support tray icons")
        super().__init__(**kwargs)

    def _bananagui_set_tooltip(self):
        pass
import tkinter as tk

from . import mainloop


class BaseWindow:

    def __init__(self, **kwargs):
        widget = self['real_widget']
        widget.title(self['title'])
        widget.bind('<Configure>', self.__configure)
        widget.protocol('WM_DELETE_WINDOW', self.__delete_window)
        super().__init__(**kwargs)

    def __configure(self, event):
        self.size.raw_set((event.width, event.height))

    def __delete_window(self):
        self.on_destroy.emit()

    def _bananagui_set_title(self, title):
        self['real_widget'].title(title)

    def _bananagui_set_resizable(self, resizable):
        self['real_widget'].resizable(resizable, resizable)

    def _bananagui_set_size(self, size):
        self['real_widget'].geometry('%dx%d' % size)

    def _bananagui_set_minimum_size(self, size):
        if size is None:
            # Default minimum size.
            size = (1, 1)
        self['real_widget'].minsize(*size)

    def _bananagui_set_showing(self, showing):
        if showing:
            self['real_widget'].deiconify()
        else:
            self['real_widget'].withdraw()

    def wait(self):
        self['real_widget'].wait_window()

    def destroy(self):
        try:
            self['real_widget'].destroy()
        except tk.TclError:
            # The widget has already been destroyed.
            pass


class Window:

    def __init__(self, **kwargs):
        widget = tk.Toplevel(mainloop.root)
        self.real_widget.raw_set(widget)
        super().__init__(**kwargs)
