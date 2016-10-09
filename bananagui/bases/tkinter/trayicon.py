import warnings


class TrayIcon:

    def __init__(self, iconpath):
        warnings.warn("Tkinter doesn't support tray icons")
        super().__init__()
