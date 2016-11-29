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

import ctypes.util

import bananagui


def _get_library(name):
    filename = ctypes.util.find_library(name)
    if filename is None:
        raise ValueError("%r is not installed" % name)
    return ctypes.CDLL(filename)


gtk = _get_library('gtk-x11-2')  # TODO: windows?
gdk = _get_library('gdk-x11-2')
glib = _get_library('glib-2')
gobject = _get_library('gobject-2')

c_int_p = ctypes.POINTER(ctypes.c_int)
gtk.g_signal_connect_data.restype = ctypes.c_ulong
gtk.gtk_adjustment_new.argtypes = [ctypes.c_double] * 6
gtk.gtk_entry_get_text.restype = ctypes.c_char_p
GCallback = ctypes.CFUNCTYPE(ctypes.c_void_p)

# These functions return widgets, but their restype is c_int by default
# which isn't guaranteed to be large enough for pointers.
for func in (
  gtk.gtk_button_new, gtk.gtk_bin_get_child, gtk.gtk_adjustment_new,
  gtk.gtk_scrolled_window_new, gtk.gtk_hbox_new, gtk.gtk_vbox_new,
  gtk.gtk_entry_new, gtk.gtk_text_view_new, gtk.gtk_text_view_get_buffer):
    func.restype = ctypes.c_void_p


# This can save a lot of head-scratching...
_dont_garbage_collect = []


def _connect(real_widget, signalname, callback):
    # This is based on glib-2.0/gobject/gsignal.h.
    real_callback = GCallback(callback)
    _dont_garbage_collect.append(real_callback)
    return gobject.g_signal_connect_data(
        real_widget, signalname.encode('utf-8'),
        real_callback, 0, 0, 0)


# These flags were generated with gtk2-constants/constants.c in the
# BananaGUI source.
GTK_WINDOW_TOPLEVEL = 0
GTK_ORIENTATION_HORIZONTAL = 0
GTK_ORIENTATION_VERTICAL = 1
GTK_JUSTIFY_CENTER = 2
GTK_DIALOG_MODAL = 1
GTK_BUTTONS_NONE = 0
GTK_MESSAGE_INFO = 0
GTK_MESSAGE_WARNING = 1
GTK_MESSAGE_ERROR = 3
GTK_MESSAGE_QUESTION = 2
