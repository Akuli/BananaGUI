import functools

from gi.repository import Gdk, Gtk

import bananagui
from . import GTK_VERSION


class Dialog:

    def __init__(self, parentwindow, **kwargs):
        widget = Gtk.Dialog(transient_for=parentwindow['real_widget'])

        # Gtk's dialogs have an action area for buttons that we don't
        # need. Let's set its border width to zero to make it invisible.
        if not widget.get_action_area.is_deprecated():
            widget.get_action_area().set_border_width(0)

        self.real_widget.raw_set(widget)
        super().__init__(**kwargs)

    # The content area needs to contain the child.
    def _bananagui_set_child(self, child):
        content = self['real_widget'].get_content_area()
        if self['child'] is not None:
            content.remove(self['child']['real_widget'])
        if child is not None:
            # The content area is a vertical box.
            content.pack_start(child['real_widget'], True, True, 0)
            child['real_widget'].show()

    def wait(self):
        # Currently I have no idea how this can be done with a regular
        # window, but it's easier with dialogs.
        self['real_widget'].run()


def _messagedialog(icon, parentwindow, message, title,
                   buttons, defaultbutton):
    # The start=100 avoids confusing this with Gtk's ResponseTypes.
    texts_and_ids = []
    for the_id, text in enumerate(buttons, start=100):
        texts_and_ids.extend([text, the_id])

    dialog = Gtk.MessageDialog(
        parentwindow['real_widget'], Gtk.DialogFlags.MODAL, icon,
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
    kwargs = {'transient_for': parentwindow['real_widget'],
              'title': title}
    if GTK_VERSION > (3, 4):
        dialog = Gtk.ColorChooserDialog(rgba=default_rgba, **kwargs)
        get_rgba = dialog.get_rgba
    else:
        # This is deprecated, but the documentation doesn't say when it
        # became deprecated and things like
        # Gtk.ColorSelectionDialog.new.is_deprecated() return False.
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
