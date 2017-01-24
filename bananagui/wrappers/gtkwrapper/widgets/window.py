# Copyright (c) 2016-2017 Akuli

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

from gi.repository import Gdk, GLib, Gtk

from .. import GTK_VERSION
from .parents import Bin


class _BaseWindow(Bin):

    def __init__(self, bananawidget):
        self.widget.set_border_width(5)  # Looks nicer.
        self.widget.connect('configure-event', self._do_configure_event)
        self.widget.connect('delete-event', self._do_delete_event)
        self.widget.show()
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
        self.widget.set_title(title)

    # TODO: resizable and size don't work correctly if resizable is
    # False but size is set.
    def set_resizable(self, resizable):
        self.widget.set_resizable(resizable)

    def set_size(self, size):
        self.widget.resize(*size)

    def set_minimum_size(self, size):
        width, height = size
        if width == 0:
            width = -1
        if height == 0:
            height = -1
        self.widget.set_size_request(width, height)

    def set_hidden(self, hidden):
        if hidden:
            self.widget.hide()
        else:
            self.widget.show()

    def close(self):
        self.widget.destroy()

    def focus(self):
        self.widget.present()


class Window(_BaseWindow):

    def __init__(self, bananawidget, title):
        self.widget = Gtk.Window(title=title)
        self._waitloop = None
        super().__init__(bananawidget)

    def close(self):
        if self._waitloop is not None:
            self._waitloop.quit()
        self.widget.destroy()

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
        self.widget = Gtk.Dialog(
            title=title, transient_for=parentwindow.widget)

        # Gtk's dialogs have an action area for buttons that we don't
        # need. Let's set its border width to zero to make it invisible
        # if direct access to it isn't deprecated.
        if GTK_VERSION < (3, 12):
            self.widget.get_action_area().set_border_width(0)

        super().__init__(bananawidget)

    # The content area needs to contain the child.
    def set_child(self, child):
        content = self.widget.get_content_area()
        if self.child is not None:
            content.remove(self.child.widget)
        if child is not None:
            # The content area is a vertical box.
            content.pack_start(child.widget, True, True, 0)
            child.widget.show()

    def wait(self):
        self.widget.run()
