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

import bananagui.color
from .. import GTK_VERSION
from .containers import Bin


class _BaseWindow(Bin):

    def __init__(self, bananawidget):
        self.real_widget.set_border_width(5)  # Looks nicer.
        self.real_widget.connect('configure-event', self._do_configure_event)
        self.real_widget.connect('delete-event', self._do_delete_event)
        self.real_widget.show()
        super().__init__(bananawidget)

    def _do_configure_event(self, widget, event):
        # The window is smaller than the minimum size when it's not
        # fully created yet, so we need to ignore that here.
        width, height = widget.get_size()
        minwidth, minheight = self.bananawidget.minimum_size
        if width >= minwidth and height >= minheight:
            self.bananawidget.size = (width, height)

    def _do_delete_event(self, widget, event):
        self.bananawidget.on_close.run()
        return True     # Block GTK's event handling.

    def set_title(self, title):
        self.real_widget.set_title(title)

    # TODO: resizable and size don't work correctly if resizable is
    # False but size is set.
    def set_resizable(self, resizable):
        self.real_widget.set_resizable(resizable)

    def set_size(self, size):
        self.real_widget.resize(*size)

    def set_minimum_size(self, size):
        width, height = size
        if width == 0:
            width = -1
        if height == 0:
            height = -1
        self.real_widget.set_size_request(width, height)

    def set_hidden(self, hidden):
        if hidden:
            self.real_widget.hide()
        else:
            self.real_widget.show()

    def close(self):
        self.real_widget.destroy()

    def focus(self):
        self.real_widget.present()


class Window(_BaseWindow):

    def __init__(self, bananawidget, title):
        self.real_widget = Gtk.Window(title=title)
        self._waitloop = None
        super().__init__(bananawidget)

    def close(self):
        if self._waitloop is not None:
            self._waitloop.quit()
        self.real_widget.destroy()

    def wait(self):
        # This is based on gtk_dialog_run in the GtkDialog C source
        # code, but this is a lot shorter because this only connects
        # delete-event and this doesn't restore the dialog to what it
        # was before running this.
        # https://github.com/GNOME/gtk/blob/master/gtk/gtkdialog.c
        self._waitloop = GLib.MainLoop()
        Gdk.threads_leave()
        self._waitloop.run()
        Gdk.threads_enter()


class Dialog(_BaseWindow):

    def __init__(self, bananawidget, parentwindow, title):
        self.real_widget = Gtk.Dialog(
            title=title, transient_for=parentwindow.real_widget)

        # Gtk's dialogs have an action area for buttons that we don't
        # need. Let's set its border width to zero to make it invisible
        # if direct access to it isn't deprecated.
        if GTK_VERSION < (3, 12):
            self.real_widget.get_action_area().set_border_width(0)

        super().__init__(bananawidget)

    # The content area needs to contain the child.
    def set_child(self, child):
        content = self.real_widget.get_content_area()
        if self.child is not None:
            content.remove(self.child.real_widget)
        if child is not None:
            # The content area is a vertical box.
            content.pack_start(child.real_widget, True, True, 0)
            child.real_widget.show()

    def wait(self):
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
    divided = [value / 255 for value in bananagui.color.hex2rgb(default)]
    default_rgba = Gdk.RGBA(*divided)
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
        result = bananagui.color.rgb2hex(rgb)
    else:
        result = None
    dialog.destroy()
    return result


def fontdialog(parentwindow, default, title):
    raise NotImplementedError  # TODO
