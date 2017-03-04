from gi.repository import Gdk, Gtk

from bananagui import color
from . import GTK_VERSION


icons = {'info': Gtk.MessageType.INFO,
         'warning': Gtk.MessageType.WARNING,
         'error': Gtk.MessageType.ERROR,
         'question': Gtk.MessageType.QUESTION}


def message(iconname, parentwindow, message, title,
            buttons, defaultbutton):
    # The start=100 avoids confusing this with Gtk's ResponseTypes.
    texts_and_ids = []
    for the_id, text in enumerate(buttons, start=100):
        texts_and_ids.append(text)
        texts_and_ids.append(the_id)

    dialog = Gtk.MessageDialog(
        parentwindow.real_widget, Gtk.DialogFlags.MODAL,
        icons[iconname], tuple(texts_and_ids), message, title=title)
    response = dialog.run()
    dialog.destroy()

    try:
        return buttons[response - 100]
    except IndexError:
        # The window was probably closed.
        return None


def colordialog(parentwindow, defaultcolor, title):
    # Gdk.RGBA uses 1 as a maximum value.
    default_rgb = (value / 255 for value in color.hex2rgb(defaultcolor))
    default_rgba = Gdk.RGBA(*default_rgb)
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
        rgb = (int(value * 255)
               for value in (rgba.red, rgba.green, rgba.blue))
        result = color.rgb2hex(rgb)
    else:
        result = None
    dialog.destroy()
    return result


# TODO: fontdialog.
