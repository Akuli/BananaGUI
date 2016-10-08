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
import warnings

# TODO: Implement better tooltips and stop relying on idlelib.
#       idlelib's tooltips fail when there are two widgets inside each
#       other. This window would display two tooltips if I would move
#       the mouse first on the window but outside the button, wait for a
#       tooltip and then move the mouse on the button:
#
#       ,------------------------------.
#       |                  | _ |[o]| X |
#       |------------------------------|
#       |         ,----------.         |
#       |         |  Button  |         |
#       |         `----------'         |
#       |                              |
#       |                              |
#       |                              |
#       `------------------------------'
_has_tooltips = True
try:
    from idlelib.ToolTip import ToolTipBase
except ImportError:
    try:
        # Maybe idlelib's modules will be renamed later?
        from idlelib.tooltip import ToolTipBase
    except ImportError:
        ToolTipBase = object
        _has_tooltips = False

from .containers import HBox, VBox  # noqa


class _ToolTip(ToolTipBase):
    """Tooltips for tkinter using idlelib.

    http://stackoverflow.com/a/30021542
    """

    def __init__(self, widget):
        """Initialize the tooltip.

        By default, this doesn't do anything. Set the text attribute
        to a string to display a tooltip.
        """
        if _has_tooltips:
            super().__init__(widget)
        else:
            warnings.warn("idlelib is required to display tkinter tooltips")
        self.text = None

    def showcontents(self):
        """Show the tooltip."""
        if self.text is not None and _has_tooltips:
            # With my dark GTK+ theme, the original showcontents
            # creates light text on a light background. This
            # always creates black text on a white background.
            label = tk.Label(
                self.tipwindow,
                text=self.text,
                # justify='left',
                foreground='black',
                background='white',
                # relief='solid',
                # borderwidth=1,
            )
            label.pack()


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


class Child:

    def __init__(self):
        super().__init__()
        self.__tooltip = None
        self._bananagui_tkinter_packed = False  # See also layouts.py.

    def _bananagui_set_expand(self, expand):
        if self._bananagui_tkinter_packed:
            # Update the pack expanding. By having this here we can make
            # sure that the pack options are changed when the expand is
            # changed.
            pack_kwargs = {'fill': _tkinter_fills[expand]}
            box_orientation = getattr(self['parent'],
                                      '_bananagui_tkinter_orientation',
                                      None)
            if box_orientation == 'h':
                # It's a HBox.
                pack_kwargs['expand'] = expand[0]
            elif box_orientation == 'v':
                # It's a VBox.
                pack_kwargs['expand'] = expand[1]
            else:
                # It's something else.
                pack_kwargs['expand'] = (expand == (True, True))
            self['real_widget'].pack(**pack_kwargs)

    def _bananagui_set_tooltip(self, tooltip):
        if self.__tooltip is None and tooltip is not None:
            self.__tooltip = _ToolTip(self['real_widget'])
        self.__tooltip.text = tooltip

    def _bananagui_set_grayed_out(self, grayed_out):
        self['real_widget']['state'] = 'disable' if grayed_out else 'normal'


class Dummy:

    def __init__(self, parent):
        super().__init__(parent)
        self.real_widget.raw_set(tk.Frame(parent['real_widget']))
