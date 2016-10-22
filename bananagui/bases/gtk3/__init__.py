"""BananaGUI GTK+ 3 base."""

# flake8: noqa

import gi

import bananagui

try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    gi.require_version('GLib', '2.0')
except ValueError as e:
    # BananaGUI expects an ImportError.
    raise ImportError from e

try:
    gi.require_version('AppIndicator3', '0.1')
    HAS_APPINDICATOR = True
except ValueError:
    HAS_APPINDICATOR = False

from gi.repository import Gtk

GTK_VERSION = (Gtk.MAJOR_VERSION, Gtk.MINOR_VERSION, Gtk.MICRO_VERSION)
orientations = {
    bananagui.HORIZONTAL: Gtk.Orientation.HORIZONTAL,
    bananagui.VERTICAL: Gtk.Orientation.VERTICAL,
}

from .basewidgets import Widget, Parent, Child
from .buttons import BaseButton, Button, ImageButton
from .canvas import Canvas
from .containers import Bin, Box
from .labels import BaseLabel, Label, ImageLabel
from .mainloop import init, main, quit, add_timeout
from .misc import (Checkbox, Dummy, Separator, set_clipboard_text,
                   get_clipboard_text, get_font_families)
from .progress import Progressbar, BouncingProgressbar, Spinner
from .ranged import Slider, Spinbox
from .textwidgets import TextBase, Entry, PlainTextView
from .trayicon import TrayIcon
from .window import (BaseWindow, Window, Dialog, infodialog, warningdialog,
                     errordialog, questiondialog, colordialog, fontdialog)
