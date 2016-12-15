# Copyright (c) 2016 Akuli

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
    GOT_APPINDICATOR = True
except ValueError:
    GOT_APPINDICATOR = False

from gi.repository import Gtk

GTK_VERSION = (Gtk.MAJOR_VERSION, Gtk.MINOR_VERSION, Gtk.MICRO_VERSION)
orientations = {
    bananagui.HORIZONTAL: Gtk.Orientation.HORIZONTAL,
    bananagui.VERTICAL: Gtk.Orientation.VERTICAL,
}
