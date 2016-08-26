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

"""Tkinter wrapper for BananaGUI."""

import contextlib
import tkinter as tk
import warnings

try:
    from idlelib.ToolTip import ToolTipBase
except ImportError:
    ToolTipBase = None


# Module-level functions
# ~~~~~~~~~~~~~~~~~~~~~~

def init():
    global _root
    _root = tk.Tk()
    _root.withdraw()


def add_timeout(time, function):
    def callback():
        if function():# == bananagui.RUN_AGAIN:
            add_timeout(time, function)
    _root.after(time, callback)


def main():
    _root.mainloop()


def quit(*args):
    _root.destroy()


# Base classes
# ~~~~~~~~~~~~

class _ToolTip(ToolTipBase or object):
    """Tooltips for tkinter using idlelib.

    http://stackoverflow.com/a/30021542
    """

    def __init__(self, widget):
        """Initialize the tooltip.

        By default, this doesn't do anything. Set the text attribute to
        a string to display a tooltip.
        """
        if ToolTipBase is None:
            warnings.warn("idlelib is required to display tooltips")
        else:
            super().__init__(widget)
        self.text = None

    def showcontents(self):
        """Show the tooltip."""
        if self.text is not None and ToolTipBase is not None:
            # With my dark GTK+ theme, the original showcontents creates
            # light text on light background. This always creates black
            # text on white background.
            label = tk.Label(
                self.tipwindow,
                text=self.text,
                #justify='left',
                foreground='black',
                background='white',
                #relief='solid',
                #borderwidth=1,
            )
            label.pack()


class WidgetBase:

    def _bananagui_set_tooltip(self, tooltip):
        # The _ToolTip instance is created here because the __init__ is
        # called before the real_widget property is set, and the
        # warning about missing idlelib will not be warned if tooltips
        # are never used.
        if tooltip is not None and not hasattr(self, '__tkinter_tooltip'):
            self.__tkinter_tooltip = _ToolTip(self['real_widget'])
        self.__tkinter_tooltip.text = tooltip


# TODO: Are empty classes required?
class ParentBase:
    pass


class ChildBase:

    def _bananagui_set_grayed_out(self, grayed_out):
        state = 'disable' if grayed_out else 'normal'
        self['real_widget'].config(state=state)


class BinBase:

    def _bananagui_set_child(self, child):
        super()._bananagui_set_child(child)
        if self['child'] is not None:
            self['child']['real_widget'].pack_forget()
        if child is not None:
            child['real_widget'].pack(fill='both', expand=True)


# Labels
# ~~~~~~

class LabelBase:

    def __init__(self, parent):
        super().__init__(parent)
        self.raw_set('real_widget', tk.Label(parent['real_widget']))


class Label:

    def _bananagui_set_text(self, text):
        self['real_widget'].config(text=text)


# Buttons
# ~~~~~~~

class ButtonBase:
    pass


class Button:

    def __init__(self, parent):
        super().__init__(parent)
        widget = tk.Button(parent['real_widget'], command=self.__on_click)
        self.raw_set('real_widget', widget)

    def __on_click(self):
        self.emit('on_click')

    def _bananagui_set_text(self, text):
        self['real_widget'].config(text=text)


# Checkbox
# ~~~~~~~~

class Checkbox:

    def __init__(self, parent):
        super().__init__(parent)

        self.__var = tk.IntVar()
        self.__var.trace('w', self.__var_changed)

        # The checkboxes have white foreground on a white background by
        # default with my dark GTK+ theme. That's why the selectcolor is
        # set to the system's default background color.
        widget = tk.Checkbutton(parent['real_widget'],
                                selectcolor=_root['bg'],
                                variable=self.__var)
        self.raw_set('real_widget', widget)

    def __var_changed(self, name, empty_string, mode):
        self.raw_set('checked', bool(self.__var.get()))

    def _bananagui_set_text(self, text):
        self['real_widget'].config(text=text)

    def _bananagui_set_checked(self, checked):
        self.__var.set(checked)


# Text widgets
# ~~~~~~~~~~~~

class TextBase:  # TODO: rename 2 EditableBase
    pass


class Entry:

    def __init__(self, parent):
        super().__init__(parent)
        self.__var = tk.StringVar()
        self.__var.trace('w', self.__var_changed)
        widget = tk.Entry(parent['real_widget'], textvariable=self.__var)
        widget.bind('<Control-A>', self.__select_all)
        widget.bind('<Control-a>', self.__select_all)
        self.raw_set('real_widget', widget)

    def __var_changed(self, name, empty_string, mode):
        self.raw_set('text', self.__var.get())

    def __select_all(self, event):
        event.widget.selection_range(0, 'end')
        return 'break'

    def _bananagui_set_text(self, text):
        self.__var.set(text)


class TextView:

    def __init__(self, parent):
        # TODO: Add more keyboard shortcuts.
        super().__init__(parent)

        # A larger width or height would prevent the widget from
        # shrinking when needed.
        widget = tk.Text(parent['real_widget'], width=1, height=1)
        widget.bind('<Control-A>', self.__select_all)
        widget.bind('<Control-a>', self.__select_all)
        widget.bind('<<Modified>>', self.__modified)
        self.raw_set('real_widget', widget)

    def __select_all(self, event):
        # The end-1c doesn't get the last character, which is a newline.
        event.widget.tag_add('sel', 1.0, 'end-1c')
        return 'break'

    def __modified(self, event):
        self.raw_set('text', event.widget.get(0.0, 'end-1c'))
        event.widget.unbind('<<Modified>>')
        event.widget.edit_modified(False)
        event.widget.bind('<<Modified>>', self.__modified)

    def _bananagui_set_text(self, text):
        self['real_widget'].delete(0.0, 'end')
        self['real_widget'].insert(0.0, text)


# Layout widgets
# ~~~~~~~~~~~~~~

class BoxBase:

    def __init__(self, parent):
        super().__init__(parent)
        self.raw_set('real_widget', tk.Frame(parent['real_widget']))

    def __get_pack_kwargs(self, startorend, expand):
        sides = {
            # (orientation, startorend): side
            ('h', 'start'): 'left',
            ('h', 'end'): 'right',
            ('v', 'start'): 'top',
            ('v', 'end'): 'bottom',
        }
        fills = {
            # (orientation, expand): fill
            ('h', True): 'both',
            ('v', True): 'both',
            ('h', False): 'y',
            ('v', False): 'x',
        }

        orientation = type(self)._bananagui_tkinter_orientation
        return {
            'side': sides[(orientation, startorend)],
            'fill': fills[(orientation, expand)],
            'expand': expand,
        }

    def add_start(self, child, expand=False):
        kwargs = self.__get_pack_kwargs('start', expand)
        child['real_widget'].pack(**kwargs)
        super().add_start(child, expand=expand)

    def add_end(self, child, expand=False):
        kwargs = self.__get_pack_kwargs('end', expand)
        child['real_widget'].pack(**kwargs)
        super().add_end(child, expand=expand)

    def remove(self, child):
        child['real_widget'].pack_forget()
        super().remove(child)

    def clear(self, child):
        # This must be before the super call because the super call
        # clears the child list.
        for child in self['children']:
            child['real_widget'].pack_forget()
        super().clear()


class HBox:
    _bananagui_tkinter_orientation = 'h'


class VBox:
    _bananagui_tkinter_orientation = 'v'


# Window classes
# ~~~~~~~~~~~~~~

class WindowBase:

    def __init__(self):
        super().__init__()
        self['real_widget'].protocol('WM_DELETE_WINDOW', self.destroy)
        self['real_widget'].title(self['title'])

        # Tkinter uses the size of the screen as the default maximum
        # size. Let's save it so we can restore it later.
        self.__default_maxsize = self['real_widget'].maxsize()

    def destroy(self):
        if self['destroyed']:
            return
        super().destroy()
        try:
            self['real_widget'].destroy()
        except tk.TclError:
            # The widget has already been destroyed.
            pass

    def _bananagui_set_title(self, title):
        self['real_widget'].title(title)

    def _bananagui_set_resizable(self, resizable):
        self['real_widget'].resizable(resizable, resizable)

    def _bananagui_set_size(self, size):
        # The size has been converted to a tuple when this is called.
        self['real_widget'].geometry('%sx%s' % size)

    def _bananagui_set_minimum_size(self, size):
        if size is None:
            # Tkinter uses (1, 1) as a default minimum size.
            size = (1, 1)
        self['real_widget'].minsize(*size)


class Window:

    def __init__(self):
        self.raw_set('real_widget', tk.Toplevel(_root))
        super().__init__()


class ChildWindow:

    def __init__(self, parent):
        self.raw_set('real_widget', tk.Toplevel(parent['real_widget']))
        super().__init__(parent)
