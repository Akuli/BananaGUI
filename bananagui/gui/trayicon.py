import bananagui
from bananagui import _base
from . import bases


class TrayIcon(_base.TrayIcon, bases.Widget):
    """An application indicator that will be displayed in the system tray."""

    # TODO: the trayicon's size shouldn't be hard-coded.
    iconpath = bananagui.Property.imagepath(
        'iconpath', settable=False,
        doc="""A path to the icon that will be displayed in the system tray.

        The icon should be 22 pixels wide and 22 pixels high.
        """)
    tooltip = bananagui.Property(
        'tooltip', type=str, allow_none=True, default=None,
        doc="""The trayicon's tooltip.

        Note that the tooltip is not displayed on some platforms.
        """)
    # TODO: A menu property, but not an on_click property. This will be
    #       an indicator instead of a tray icon on some platforms.
