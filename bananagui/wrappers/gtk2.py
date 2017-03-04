# flake8: noqa

"""Set up gtkwrapper for GTK+ 3 and replace this module with it."""

import sys
import warnings
import gi

# Ignore the GTK+ 2 warning.
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    gi.require_version('Gtk', '2.0')
    from gi.repository import Gtk

gi.require_version('Gdk', '2.0')
gi.require_version('GLib', '2.0')

from . import gtkwrapper
sys.modules[__name__] = gtkwrapper
