"""BananaGUI GTK+ 3 base."""

# flake8: noqa

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GLib', '2.0')

try:
    gi.require_version('AppIndicator3', '0.1')
    has_appindicator = True
except ValueError:
    has_appindicator = False

from .bases import Widget, Parent, Child, Dummy
from .buttons import BaseButton, Button, ImageButton
from .canvas import Canvas
from .checkbox import Checkbox
from .containers import Bin, Box, HBox, VBox
from .labels import BaseLabel, Label, ImageLabel
from .mainloop import init, main, quit
from .textwidgets import TextBase, Entry, PlainTextView
from .trayicon import TrayIcon
from .windows import BaseWindow, Window, Dialog, messagedialog

from .clipboard import set_clipboard_text, get_clipboard_text
from .timeouts import add_timeout
