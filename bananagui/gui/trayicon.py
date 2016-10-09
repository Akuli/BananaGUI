from bananagui import _base, Property
from .bases import Widget


class TrayIcon(_base.TrayIcon, Widget):
    """An application indicator that will be displayed in the system tray."""

    # TODO: the trayicon's size shouldn't be hard-coded.
    iconpath = Property.imagepath(
        'iconpath', settable=False,
        doc="""A path to the icon that will be displayed in the system tray.

        The icon should be 22 pixels wide and 22 pixels high.
        """)
    tooltip = Property(
        'tooltip', type=str, allow_none=True, default=None,
        doc="""The trayicon's tooltip.

        Note that the tooltip is not displayed on some platforms.
        """)
    # TODO: A menu property, but not an on_click property. This will be
    #       an indicator instead of a tray icon on some platforms.

    def __init__(self, iconpath: str, **kwargs):
        """Initialize the tray icon.

        The icon path needs to be given on initialization because some
        GUI toolkits need to know it before creating a tray icon. A tray
        icon without an icon would also be quite useless.
        """
        self.iconpath.raw_set(iconpath)
        # The base needs to call super().__init__ with no positional
        # arguments.
        super().__init__(iconpath, **kwargs)
