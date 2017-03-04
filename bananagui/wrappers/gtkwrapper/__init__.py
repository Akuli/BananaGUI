"""Non-public BananaGUI wrapper for GTK+."""

# flake8: noqa

import gi

import bananagui

try:
    gi.require_version('AppIndicator3', '0.1')
    GOT_APPINDICATOR = True
except ValueError:
    GOT_APPINDICATOR = False

from gi.repository import Gtk

GTK_VERSION = (Gtk.MAJOR_VERSION, Gtk.MINOR_VERSION, Gtk.MICRO_VERSION)
