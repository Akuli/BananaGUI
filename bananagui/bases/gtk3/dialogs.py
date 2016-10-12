from gi.repository import Gdk, Gtk

from bananagui import Color
from . import _GTK_VERSION


class Dialog:

    def __init__(self, parentwindow, **kwargs):
        self.real_widget.raw_set(Gtk.Dialog(parentwindow['real_widget']))
        super().__init__(**kwargs)


def messagedialog(icon, parentwindow, text, title, buttons, defaultbutton):
    raise NotImplementedError  # TODO


def colordialog(parentwindow, default, title):
    default_rgba = Gdk.RGBA(default.red/255,
                            default.green/255,
                            default.blue/255)
    kwargs = {'transient_for': parentwindow['real_widget'],
              'title': title}
    if _GTK_VERSION[:2] > (3, 4):
        # This is new in GTK+ 3.4.
        dialog = Gtk.ColorChooserDialog(rgba=default_rgba, **kwargs)
        get_rgba = dialog.get_rgba
    else:
        # This is deprecated, but the documentation doesn't say when it
        # became deprecated.
        # https://developer.gnome.org/gtk3/stable/GtkColorSelectionDialog.html
        dialog = Gtk.ColorSelectionDialog(**kwargs)
        selection = dialog.get_color_selection()
        selection.set_current_rgba(default_rgba)
        get_rgba = selection.get_current_rgba

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        result = Color.from_rgbstring(get_rgba().to_string())
    else:
        result = None
    dialog.destroy()
    return result


def fontdialog(parentwindow, default, title):
    raise NotImplementedError  # TODO
