"""BananaGUI GTK+ 3 base."""

# flake8: noqa

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GLib', '2.0')

try:
    gi.require_version('AppIndicator3', '0.1')
    HAS_APPINDICATOR = True
except ValueError:
    HAS_APPINDICATOR = False

from gi.repository import Gtk
GTK_VERSION = (Gtk.MAJOR_VERSION, Gtk.MINOR_VERSION, Gtk.MICRO_VERSION)

from .bases import Widget, Parent, Child
from .buttons import BaseButton, Button, ImageButton
from .canvas import Canvas
from .clipboard import set_clipboard_text, get_clipboard_text
from .containers import Bin, Box
from .dialogs import (Dialog, infodialog, warningdialog, errordialog,
                      colordialog, fontdialog)
from .labels import BaseLabel, Label, ImageLabel
from .mainloop import init, main, quit
from .misc import (Checkbox, Dummy, Separator, Spinner, Spinbox, Slider,
                   Progressbar, get_font_families)
from .textwidgets import TextBase, Entry, PlainTextView
from .timeouts import add_timeout
from .trayicon import TrayIcon
from .window import BaseWindow, Window
