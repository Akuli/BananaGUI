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

"""Base classes."""

import tkinter as tk

try:
    from idlelib.ToolTip import ToolTipBase
except ImportError:
    try:
        # Maybe idlelib's modules will be renamed later?
        from idlelib.tooltip import ToolTipBase
    except ImportError:
        ToolTipBase = None


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
            warnings.warn("idlelib is required to display tkinter tooltips")
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
    pass


class ParentBase:
    pass


class ChildBase:

    def __init__(self):
        super().__init__()
        self.__tkinter_tooltip = None

    def _bananagui_set_tooltip(self, tooltip):
        if self.__tkinter_tooltip is None and tooltip is not None:
            self.__tkinter_tooltip = _ToolTip(self['real_widget'])
        self.__tkinter_tooltip.text = tooltip

    def _bananagui_set_grayed_out(self, grayed_out):
        state = 'disable' if grayed_out else 'normal'
        self['real_widget'].config(state=state)


class BinBase:

    def _bananagui_set_child(self, child):
        if self['child'] is not None:
            self['child']['real_widget'].pack_forget()
        if child is not None:
            child['real_widget'].pack(fill='both', expand=True)
