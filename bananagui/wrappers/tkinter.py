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
        if self.text is None:
            return
        else:
            # With my dark GTK+ theme, the original showcontents creates
            # light text on light background. This always creates black
            # text on white background.
            label = tk.Label(self.tipwindow, text=self.text, justify='left',
                             foreground='black', background='white',
                             relief='solid', borderwidth=1)
            label.pack()


class Widget(widgets.Widget):

    __doc__ = widgets.Widget.__doc__

    @functools.wraps(widgets.Widget.__init__)
    def __init__(self):
        super().__init__()
        self.props['tooltip'].setter = self.__set_tooltip

    def __set_tooltip(self, tooltip):
        # The _ToolTip instance is created here because the __init__()
        # is called before the real_widget() property has a value.
        if idlelib is None and tooltip is not None:
            warnings.warn("idlelib is required to display tooltips")
        else:
            if not hasattr(self, '__tooltip'):
                self.__tooltip = _ToolTip(self['real_widget'])
            self.__tooltip.text = tooltip

    @functools.wraps(widgets.Widget.__del__)
    def __del__(self):
        if self['real_widget'] is not None:
            try:
                self['real_widget'].destroy()
            except tk.TclError:
                # The widget has probably been destroyed already.
                pass


class Bin(widgets.Bin, Widget):

    __doc__ = widgets.Bin.__doc__

    @functools.wraps(widgets.Bin.__init__)
    def __init__(self):
        super().__init__()
        self.props['child'].setter = self.__set_child

    def __set_child(self, child):
        # Check if the child is already in the bin.
        if child is self['child']:
            return

        # Remove the old child if it's set.
        if self['child'] is not None:
            self['child']['real_widget'].pack_forget()

        # Check the new child and add it.
        if child is not None:
            if child['parent'] is not self:
                raise ValueError("cannot add a child with the wrong parent")
            child['real_widget'].pack(fill='both', expand=True)

        # Change the property's value.
        with self.props['child'].run_callbacks():
            self.props['child'].value = child


class Window(widgets.Window, Bin):

    __doc__ = widgets.Bin.__doc__

    @functools.wraps(widgets.Window.__init__)
    def __init__(self, parentwindow=None):
        """Initialize the window."""
        super().__init__(parentwindow=parentwindow)
        self.props['real_widget'].value = tk.Toplevel(
            _root if parentwindow is None else parentwindow)
        self['real_widget'].title(self['title'])  # Set the default title.
        self['real_widget'].protocol('WM_DELETE_WINDOW',
                                     self.__on_wm_delete_window)
        self.props['title'].setter = self['real_widget'].title
        self.props['showing'].setter = self.__set_showing
        self.props['size'].setter = self.__set_size
        self.props['width'].getter = self['real_widget'].winfo_width
        self.props['height'].getter = self['real_widget'].winfo_height

    def __on_wm_delete_window(self):
        self['showing'] = False

    def __set_showing(self, showing):
        # TODO: What if the window is minimized?
        if showing:
            self['real_widget'].deiconify()
        else:
            self['real_widget'].withdraw()

    def __set_size(self, size):
        self['real_widget'].geometry('{}x{}'.format(*size))


class Child(widgets.Child, Widget):

    __doc__ = widgets.Child.__doc__

    @functools.wraps(widgets.Child.__init__)
    def __init__(self, parent):
        super().__init__(parent)
        self.props['grayed_out'].setter = self.__set_grayed_out

    def __set_grayed_out(self, grayed_out):
        state = 'disable' if grayed_out else 'normal'
        self['real_widget'].config(state=state)


class Box(widgets.Box, Child):

    __doc__ = widgets.Box.__doc__

    @functools.wraps(widgets.Box.__init__)
    def __init__(self, parent, orientation):
        super().__init__(parent, orientation)
        self.props['real_widget'].value = tk.Frame(parent['real_widget'])

    def __get_pack_kwargs(self, method, expand):
        """Get keyword arguments for child['real_widget'].pack().

        method should be 'prepend' or 'append'.
        """
        sides = {
            # (orientation, method): size
            # These may look wrong way, but when multiple widgets are
            # packed tkinter packs the first one to the edge and works
            # its way to the center instead of pushing each new widget
            # all the way to the edge.
            ('horizontal', 'prepend'): 'right',
            ('horizontal', 'append'): 'left',
            ('vertical', 'prepend'): 'bottom',
            ('vertical', 'append'): 'top',
        }
        fills = {
            # (orientation, expand): fill
            ('horizontal', True): 'both',
            ('vertical', True): 'both',
            ('horizontal', False): 'y',
            ('vertical', False): 'x',
        }
        return {
            'side': sides[(self['orientation'], method)],
            'fill': fills[(self['orientation'], expand)],
            'expand': expand,
        }

    @functools.wraps(widgets.Box.prepend)
    def prepend(self, child, expand=False):
        super().prepend(child, expand=expand)
        kwargs = self.__get_pack_kwargs('prepend', expand)
        child['real_widget'].pack(**kwargs)

    @functools.wraps(widgets.Box.append)
    def append(self, child, expand=False):
        super().append(child, expand=expand)
        kwargs = self.__get_pack_kwargs('append', expand)
        child['real_widget'].pack(**kwargs)

    @functools.wraps(widgets.Box.remove)
    def remove(self, child):
        super().remove(child)
        child['real_widget'].pack_forget()

    @functools.wraps(widgets.Box.clear)
    def clear(self):
        # The pack_forget calls must be before the super call because
        # self['children'] is empty after the super call.
        for child in self['children']:
            child['real_widget'].pack_forget()
        super().clear()


class Label(widgets.Label, Child):

    __doc__ = widgets.Label.__doc__

    @functools.wraps(widgets.Label.__init__)
    def __init__(self, parent):
        super().__init__(parent)
        self.props['real_widget'].value = tk.Label(parent['real_widget'])
        self.props['text'].setter = self.__set_text

    def __set_text(self, text):
        self['real_widget'].config(text=text)


class ButtonBase(widgets.ButtonBase, Child):

    __doc__ = widgets.ButtonBase.__doc__

    @functools.wraps(widgets.ButtonBase.__init__)
    def __init__(self, parent):
        super().__init__(parent)
        self.props['real_widget'].value = tk.Button(
            parent['real_widget'],
            command=self.__on_click,
        )

    def __on_click(self, event=None):
        if self['on_click'] is not None:
            self['on_click']()


class TextButton(widgets.TextButton, ButtonBase):

    __doc__ = widgets.TextButton.__doc__

    @functools.wraps(widgets.TextButton.__init__)
    def __init__(self, parent):
        super().__init__(parent)
        self.props['text'].setter = self.__set_text

    def __set_text(self, text):
        self['real_widget'].config(text=text)


@functools.wraps(widgets.main)
def main():
    global _root
    _root.mainloop()
    _root = tk.Tk()
    _root.withdraw()


@functools.wraps(widgets.quit)
def quit(*args):
    _root.destroy()


_root = tk.Tk()
_root.withdraw()
