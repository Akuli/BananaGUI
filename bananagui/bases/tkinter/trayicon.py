import warnings


class TrayIcon:

    def __init__(self, iconpath, **kwargs):
        warnings.warn("Tkinter doesn't support tray icons", RuntimeWarning)
        super().__init__(**kwargs)

    def _bananagui_set_tooltip(self):
        pass
