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

"""Tkinter interface."""

import functools
import tkinter as tk
import warnings

import bananagui
from bananagui.core import widgets

try:
    import idlelib.ToolTip      # noqa
    _ToolTipBase = idlelib.ToolTip.ToolTipBase
except ImportError:
    idlelib = None
    _ToolTipBase = object


class _ToolTip(_ToolTipBase):
    """Tooltips for tkinter using idlelib.

    http://stackoverflow.com/a/30021542
    """

    def __init__(self, widget):
        """Initialize the tooltip.

        By default, this doesn't do anything. Set the text attribute to
        a string to display a tooltip.
        """
        assert idlelib is not None, "cannot create _ToolTips without idlelib"
        super().__init__(widget)
        self.text = None

    def showcontents(self):
        """Show the tooltip."""
        if self.text is not None:
            # With my dark GTK+ theme, the original showcontents creates
            # light text on light background. This always creates black
            # text on white background.
            label = tk.Label(
                self.tipwindow, text=str(self.text), justify='left',
                foreground='black', background='white', relief='solid',
                borderwidth=1,
            )
            label.pack()


class Widget(widgets.Widget):

    __doc__ = widgets.Widget.__doc__

    @functools.wraps(widgets.Widget.set_tooltip)
    def set_tooltip(self, tooltip):
        # The _ToolTip instance is created here because the __init__()
        # is called before the real_widget() property has a _value.
        if idlelib is None and tooltip is not None:
            warnings.warn("idlelib is required to display tooltips",
                          bananagui.MissingFeatureWarning)
        else:
            if not hasattr(self, '__tkinter_tooltip'):
                self.__tkinter_tooltip = _ToolTip(self['real_widget'])
            self.__tkinter_tooltip.text = tooltip
        super().set_tooltip(tooltip)


class Bin(widgets.Bin, Widget):

    __doc__ = widgets.Bin.__doc__

    @functools.wraps(widgets.Bin.set_child)
    def set_child(self, child):
        if self.get_child() is not None:
            self.get_child().get_real_widget().pack_forget()
        if child is not None:
            child.get_real_widget().pack(fill='both', expand=True)
        super().set_child(child)


class Window(widgets.Window, Bin):

    __doc__ = widgets.Bin.__doc__

    @functools.wraps(widgets.Window.__init__)
    def __init__(self, parentwindow=None):
        """Initialize the window."""
        super().__init__(parentwindow=parentwindow)
        widget = self.__real_widget = tk.Toplevel(
            _root if parentwindow is None else parentwindow.get_real_widget())
        widget.protocol('WM_DELETE_WINDOW', self.on_close.emit)
        widget.title(self.get_title())    # Set the default title.
        widget.bind('<Configure>', self.__on_configure)

    @functools.wraps(widgets.Widget.get_real_widget)
    def get_real_widget(self):
        return self.__real_widget

    @functools.wraps(widgets.Window.set_title)
    def set_title(self, title):
        self.get_real_widget().title(title)
        super().set_title(title)

    @functools.wraps(widgets.Window.set_size)
    def set_size(self, size):
        self.get_real_widget().geometry('{}x{}'.format(*size))
        # The configure event binding will emit the size changed signal
        # by calling super().set_size().

    def __on_configure(self, event):
        super().set_size([event.width, event.height])


class Child(widgets.Child, Widget):

    __doc__ = widgets.Child.__doc__

    @functools.wraps(widgets.Child.set_grayed_out)
    def set_grayed_out(self, grayed_out):
        state = 'disable' if grayed_out else 'normal'
        self.get_real_widget().config(state=state)


class Box(widgets.Box, Child):

    __doc__ = widgets.Box.__doc__

    @functools.wraps(widgets.Box.__init__)
    def __init__(self, parent, orientation):
        super().__init__(parent, orientation)
        self.__real_widget = tk.Frame(parent.get_real_widget())

    @functools.wraps(widgets.Box.get_real_widget)
    def get_real_widget(self):
        return self.__real_widget

    def __get_pack_kwargs(self, expand, append):
        """Get keyword arguments for child.get_real_widget().pack().

        append should be True if this is called from append and False
        otherwise.
        """
        sides = {
            # (orientation, append): size
            # These may look wrong way, but when multiple widgets are
            # packed tkinter packs the first one to the edge and works
            # its way to the center instead of pushing each new widget
            # all the way to the edge.
            (bananagui.HORIZONTAL, False): 'right',
            (bananagui.HORIZONTAL, True): 'left',
            (bananagui.VERTICAL, False): 'bottom',
            (bananagui.VERTICAL, True): 'top',
        }
        fills = {
            # (orientation, append): fill
            (bananagui.HORIZONTAL, True): 'both',
            (bananagui.HORIZONTAL, False): 'y',
            (bananagui.VERTICAL, True): 'both',
            (bananagui.VERTICAL, False): 'x',
        }
        return {
            'side': sides[(self.get_orientation(), append)],
            'fill': fills[(self.get_orientation(), expand)],
            'expand': expand,
        }

    @functools.wraps(widgets.Box.prepend)
    def prepend(self, child, expand=False):
        super().prepend(child, expand=expand)
        kwargs = self.__get_pack_kwargs(expand, append=False)
        child.get_real_widget().pack(**kwargs)

    @functools.wraps(widgets.Box.append)
    def append(self, child, expand=False):
        super().append(child, expand=expand)
        kwargs = self.__get_pack_kwargs(expand, append=True)
        child.get_real_widget().pack(**kwargs)

    @functools.wraps(widgets.Box.remove)
    def remove(self, child):
        super().remove(child)
        child.get_real_widget().pack_forget()

    @functools.wraps(widgets.Box.clear)
    def clear(self):
        # The pack_forget calls must be before the super call because
        # self['children'] is empty after the super call.
        for child in self.get_children():
            child.get_real_widget().pack_forget()
        super().clear()


class Label(widgets.Label, Child):

    __doc__ = widgets.Label.__doc__

    @functools.wraps(widgets.Label.__init__)
    def __init__(self, parent):
        super().__init__(parent)
        self.__real_widget = tk.Label(parent.get_real_widget())

    @functools.wraps(widgets.Label.get_real_widget)
    def get_real_widget(self):
        return self.__real_widget

    def set_text(self, text):
        self.get_real_widget().config(text=text)
        super().set_text(text)


class ButtonBase(widgets.ButtonBase, Child):

    __doc__ = widgets.ButtonBase.__doc__

    @functools.wraps(widgets.ButtonBase.__init__)
    def __init__(self, parent):
        super().__init__(parent)
        self.real_widget._value = tk.Button(
            parent['real_widget'],
            command=self.on_click.emit,
        )


class TextButton(widgets.TextButton, ButtonBase):

    __doc__ = widgets.TextButton.__doc__

    @functools.wraps(widgets.TextButton.__init__)
    def __init__(self, parent):
        super().__init__(parent)
        self.__real_widget = tk.Button(parent.get_real_widget())

    @functools.wraps(widgets.TextButton.get_real_widget)
    def get_real_widget(self):
        return self.__real_widget

    def set_text(self, text):
        self['real_widget'].config(text=text)


@functools.wraps(widgets.main)
def main():
    global _root
    _root.mainloop()
    _root = tk.Tk()
    _root.withdraw()


@functools.wraps(widgets.quit)
def quit():
    _root.destroy()


_root = tk.Tk()
_root.withdraw()
