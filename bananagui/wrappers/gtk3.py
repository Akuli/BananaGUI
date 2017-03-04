# flake8: noqa

"""Set up gtkwrapper for GTK+ 3 and replace this module with it."""

import sys
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GLib', '2.0')

from . import gtkwrapper
sys.modules[__name__] = gtkwrapper
