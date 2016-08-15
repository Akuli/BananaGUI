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

"""Base widgets for other widgets."""

import bananagui
from bananagui.core import bases

try:
    from idlelib.ToolTip import ToolTipBase
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
                justify='left',
                foreground='black',
                background='white',
                # relief='solid',
                borderwidth=1,
            )
            label.pack()


class WidgetBase(bases.WidgetBase):

    __doc__ = bases.WidgetBase.__doc__
    tooltip = bases.WidgetBase.tooltip.copy()

    @tooltip.setter
    def tooltip(self, tooltip):
        # The _ToolTip instance is created here because the __init__ is
        # called before the real_widget property is set, and the
        # warning about missing idlelib will not be warned if tooltips
        # are never used.
        if not hasattr(self, '__tkinter_tooltip'):
            self.__tkinter_tooltip = _ToolTip(self['real_widget'])
        self.__tkinter_tooltip.text = tooltip


class ParentBase(bases.WidgetBase):

    __doc__ = bases.ParentBase.__doc__


class ChildBase(bases.WidgetBase):

    __doc__ = bases.WidgetBase.__doc__
    grayed_out = bases.WidgetBase.grayed_out.copy()

    @grayed_out.setter
    def grayed_out(self, grayed_out):
        self['real_widget'].config(state='disable' if grayed_out else 'normal')

class BinBase(bases.BinBase):

    
