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

import ctypes
import functools

import bananagui.color
from .libs import _connect, GTK_WINDOW_TOPLEVEL, gdk, glib, gtk


class BaseWindow:

    def __init__(self, **kwargs):
        _connect(self.real_widget, 'configure-event', self._do_configure_event)
        _connect(self.real_widget, 'delete-event', self._do_delete_event)
        gtk.gtk_widget_show(self.real_widget)
        super().__init__(**kwargs)

    def _do_configure_event(self):
        width = ctypes.c_int()
        height = ctypes.c_int()
        gtk.gtk_window_get_size(
            self.real_widget, ctypes.byref(width), ctypes.byref(height))
        print('_do_configure_event', width, height)
        self.size = (width.value, height.value)

    def _do_delete_event(self):
        self.run_callbacks('on_close')
        return True     # Block GTK's delete-event handling.

    def _set_title(self, title):
        gtk.gtk_window_set_title(self.real_widget, title.encode('utf-8'))

    # TODO: resizable and size don't work correctly if resizable is
    # False but size is set.
    def _set_resizable(self, resizable):
        gtk.gtk_window_set_resizable(self.real_widget, resizable)

    def _set_size(self, size):
        # TODO: THIS IS WHY THIS IS IS BROKEN
        # https://developer.gnome.org/gtk2/stable/GtkWindow.html#gtk-window-get-size
        gtk.gtk_window_resize(self.real_widget, *size)

    def _set_minimum_size(self, size):
        width, height = size
        if width is None:
            width = -1
        if height is None:
            height = -1
        gtk.gtk_widget_set_size_request(self.real_widget, width, height)

    def _set_showing(self, showing):
        if showing:
            gtk.gtk_widget_show(self.real_widget)
        else:
            gtk.gtk_widget_hide(self.real_widget)

    def _close(self):
        gtk.gtk_widget_destroy(self.real_widget)

    def _wait(self):
        raise NotImplementedError  # TODO

    def _focus(self):
        gtk.gtk_window_present(self.real_widget)


class Window:

    def __init__(self, **kwargs):
        self.real_widget = gtk.gtk_window_new(GTK_WINDOW_TOPLEVEL)
        super().__init__(**kwargs)


class Dialog:

    def __init__(self, **kwargs):
        self.real_widget = gtk.gtk_dialog_new()
        gtk.gtk_window_set_transient_for(
            self.real_widget, self.parentwindow.real_widget)

        # We don't need the action area so we'll make it invisible.
        action_area = gtk.gtk_dialog_get_action_area(self.real_widget)
        gtk.gtk_container_set_border_width(action_area, 0)

        super().__init__(**kwargs)

    # The child needs to go to the content area.
    def _set_child(self, child):
        content = gtk.gtk_dialog_get_content_area(self.real_widget)
        if self.child is not None:
            gtk.gtk_container_remove(self.child.real_widget)
        if child is not None:
            # The content area is a vertical box.
            gtk.gtk_box_pack_start(
                self.real_widget, child.real_widget, True, True, 0)
            gtk.gtk_widget_show(child.real_widget)

    def _wait(self):
        gtk.gtk_dialog_run(self.real_widget)


def _messagedialog(messagetype, parentwindow, message, title,
                   buttons, defaultbutton):
    dialog = gtk.gtk_message_dialog_new(
        parentwindow.real_widget, 1,    # 1 is GTK_DIALOG_MODAL
        messagetype, 0, message.encode('utf-8'))

    # The start=100 avoids confusing these with GTK's ResponseTypes.
    for the_id, text in enumerate(buttons, start=100):
        gtk_dialog_add_button(dialog, text.encode('utf-8'), the_id)

    gtk_window_set_title(dialog, title.encode('utf-8'))
    response = gtk_dialog_run(dialog)
    gtk_widget_destroy(dialog)

    try:
        return buttons[response - 100]
    except IndexError:
        # The window was probably closed.
        return None


infodialog = functools.partial(_messagedialog, 0)
warningdialog = functools.partial(_messagedialog, 1)
questiondialog = functools.partial(_messagedialog, 2)
errordialog = functools.partial(_messagedialog, 3)


def colordialog(parentwindow, default, title):
    raise NotImplementedError  # TODO

def fontdialog(parentwindow, default, title):
    raise NotImplementedError  # TODO
