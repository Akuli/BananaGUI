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

"""A TrayIcon widget."""

# TODO: fix this.

import bananagui
from .basewidgets import Widget

_base = bananagui._get_base('widgets.trayicon')


class TrayIcon(_base.TrayIcon, Widget):
    """An application indicator that will be displayed in the system tray."""

    # TODO: the trayicon's size shouldn't be hard-coded.
    iconpath = bananagui.BananaProperty.imagepath(
        'iconpath', settable=False,
        doc="""A path to the icon that will be displayed in the system tray.

        The icon should be 22 pixels wide and 22 pixels high.
        """)
    tooltip = bananagui.BananaProperty(
        'tooltip', type=str, allow_none=True, default=None,
        doc="""The trayicon's tooltip.

        Note that the tooltip is not displayed on some platforms.
        """)
    # TODO: A menu property, but not an on_click property. This will be
    #       an indicator instead of a tray icon on some platforms.
