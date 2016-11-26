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

import functools

from gi.repository import Gdk, GLib, Gtk

import bananagui
from . import GTK_VERSION


class BaseWindow:

    def __init__(self, **kwargs):
        self._waitloop = None
        self.real_widget.set_title(self.title)
        self.real_widget.connect('configure-event', self._do_configure_event)
        self.real_widget.connect('delete-event', self._do_delete_event)
        self.real_widget.show()
        super().__init__(**kwargs)

    def _do_configure_event(self, widget, event):
        self.size = widget.get_size()

    def _do_delete_event(self, widget, event):
        self.run_callbacks('on_close')
        return True  # Block GTK's delete-event handling.

    def _set_title(self, title):
        self.real_widget.set_title(title)

    # TODO: resizable and size don't work correctly if resizable is
    # False but size is set.
    def _set_resizable(self, resizable):
        self.real_widget.set_resizable(resizable)

    def _set_size(self, size):
        self.real_widget.resize(*size)

    def _set_minimum_size(self, size):
        width, height = size
        if width is None:
            width = -1
        if height is None:
            height = -1
        self.real_widget.set_size_request(width, height)

    def _set_showing(self, showing):
        if showing:
            self.real_widget.show()
        else:
            self.real_widget.hide()

    def _close(self):
        if self._waitloop is not None:
            self._waitloop.quit()
        self.real_widget.destroy()

    def _wait(self):
        # This is based on gtk_dialog_run in the GtkDialog C source
        # code, but this is a lot shorter because this only connects
        # delete-event and this doesn't restore the dialog to what it
        # was before running this.
        # https://github.com/GNOME/gtk/blob/master/gtk/gtkdialog.c
        self._waitloop = GLib.MainLoop()
        Gdk.threads_leave()
        self._waitloop.run()
        Gdk.threads_enter()

    def _focus(self):
        self.real_widget.present()


class Window:

    def __init__(self, **kwargs):
        self.real_widget = Gtk.Window()
        super().__init__(**kwargs)


class Dialog:

    def __init__(self, **kwargs):
        self.real_widget = Gtk.Dialog(
            transient_for=self.parentwindow.real_widget)

        # Gtk's dialogs have an action area for buttons that we don't
        # need. Let's set its border width to zero to make it invisible
        # if direct access to it isn't deprecated.
        if GTK_VERSION < (3, 12):
            self.real_widget.get_action_area().set_border_width(0)

        super().__init__(**kwargs)

    # The content area needs to contain the child.
    def _set_child(self, child):
        content = self.real_widget.get_content_area()
        if self.child is not None:
            content.remove(self.child.real_widget)
        if child is not None:
            # The content area is a vertical box.
            content.pack_start(child.real_widget, True, True, 0)
            child.real_widget.show()

    def _wait(self):
        self.real_widget.run()


def _messagedialog(icon, parentwindow, message, title,
                   buttons, defaultbutton):
    # The start=100 avoids confusing this with Gtk's ResponseTypes.
    texts_and_ids = []
    for the_id, text in enumerate(buttons, start=100):
        texts_and_ids.append(text)
        texts_and_ids.append(the_id)

    dialog = Gtk.MessageDialog(
        parentwindow.real_widget, Gtk.DialogFlags.MODAL, icon,
        tuple(texts_and_ids), message, title=title)
    response = dialog.run()
    dialog.destroy()

    try:
        return buttons[response - 100]
    except IndexError:
        # The window was probably closed.
        return None


infodialog = functools.partial(_messagedialog, Gtk.MessageType.INFO)
warningdialog = functools.partial(_messagedialog, Gtk.MessageType.WARNING)
errordialog = functools.partial(_messagedialog, Gtk.MessageType.ERROR)
questiondialog = functools.partial(_messagedialog, Gtk.MessageType.QUESTION)


def colordialog(parentwindow, default, title):
    # Gdk.RGBA uses 0 as minimum value and 1 as maximum value.
    default_rgba = Gdk.RGBA(default.red/255,
                            default.green/255,
                            default.blue/255)
    kwargs = {'transient_for': parentwindow.real_widget,
              'title': title}
    if GTK_VERSION > (3, 4):
        # We can use the new ColorChooserDialog.
        dialog = Gtk.ColorChooserDialog(rgba=default_rgba, **kwargs)
        get_rgba = dialog.get_rgba
    else:
        # This is deprecated, but the documentation doesn't
        # say when it became deprecated and things like
        # Gtk.ColorSelectionDialog.new.is_deprecated() return False O_o
        # https://developer.gnome.org/gtk3/stable/GtkColorSelectionDialog.html
        dialog = Gtk.ColorSelectionDialog(**kwargs)
        selection = dialog.get_color_selection()
        selection.set_current_rgba(default_rgba)
        get_rgba = selection.get_current_rgba

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        rgba = get_rgba()
        rgb = [int(value * 255) for value in (rgba.red, rgba.green, rgba.blue)]
        result = bananagui.Color(*rgb)
    else:
        result = None
    dialog.destroy()
    return result


def fontdialog(parentwindow, default, title):
    raise NotImplementedError  # TODO
