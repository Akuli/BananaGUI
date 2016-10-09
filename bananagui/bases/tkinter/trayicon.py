import warnings


class TrayIcon:

    def __init__(self, iconpath):
        warnings.warn("Tkinter doesn't support tray icons")
        super().__init__()

    def _bananagui_set_tooltip(self):
        pass
