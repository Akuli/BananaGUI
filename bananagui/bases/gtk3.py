from gi.repository import Gtk


class Widget:

    def __init__(self, **kwargs):
        # I have no idea why GTK+ makes changing the background color in
        # a non-deprecated (not-removed) way such a pain.
        self.__css = {}
        self.__provider = Gtk.CssProvider()
        context = self['real_widget'].get_style_context()
        context.add_provider(self.__provider,
                             Gtk.STYLE_PROVIDER_PRIORITY_USER)
        super().__init__(**kwargs)

    def __update_css(self):
        words = []
        for item in self.__css.items():
            words.append('%s: %s;' % item)
        css = '* { %s }' % ' '.join(words)
        self.__provider.load_from_data(css.encode('utf-8'))

    def _bananagui_set_background(self, color):
        if color is None:
            try:
                del self.__css['background-color']
            except KeyError:
                pass
        else:
            self.__css['background-color'] = color.rgbstring
        self.__update_css()


class Parent:
    pass


class Child:

    def _bananagui_set_expand(self, expand):
        horizontal, vertical = expand
        self['real_widget'].set_hexpand(horizontal)
        self['real_widget'].set_vexpand(vertical)

    def _bananagui_set_grayed_out(self, grayed_out):
        self['real_widget'].set_sensitive(not grayed_out)

    def _bananagui_set_tooltip(self, tooltip):
        self['real_widget'].set_tooltip_text(tooltip)
from gi.repository import Gtk


class BaseButton:
    pass


class Button:

    def __init__(self, parent, **kwargs):
        button = Gtk.Button()
        button.connect('clicked', self.__click)
        self.real_widget.raw_set(button)
        super().__init__(parent, **kwargs)

    def __click(self, button):
        self.on_click.emit()

    def _bananagui_set_text(self, text):
        self['real_widget'].set_label(text)


class ImageButton:

    def __init__(self, parent, **kwargs):
        raise NotImplementedError  # TODO
class Canvas:

    def __init__(self, parent, **kwargs):
        raise NotImplementedError  # TODO
        super().__init__(parent, **kwargs)

    def _bananagui_set_minimum_size(self, size):
        ...

    def _bananagui_set_background(self, background):
        ...

    def draw_line(self, pos1, pos2, thickness, color):
        ...

    def draw_polygon(self, *positions, fillcolor, linecolor, linethickness):
        ...

    def draw_oval(self, centerpos, xradius, yradius, fillcolor,
                  linecolor, linethickness):
        ...
from gi.repository import Gtk, Gdk

clipboard = None


def init_clipboard():
    global clipboard
    if clipboard is None:
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)


def set_clipboard_text(text):
    init_clipboard()
    clipboard.set_text(text, -1)
    clipboard.store()


def get_clipboard_text():
    init_clipboard()
    # clipboard.wait_for_text() doesn't block if there's no text on the
    # clipboard, it returns None.
    result = clipboard.wait_for_text()
    if result is None:
        return ''
    return result
from gi.repository import Gtk

import bananagui


class Bin:

    def _bananagui_set_child(self, child):
        if self['child'] is not None:
            self['real_widget'].remove(self['child']['real_widget'])
        if child is not None:
            self['real_widget'].add(child['real_widget'])
            child['real_widget'].show()


_gtk_orientations = {
    bananagui.HORIZONTAL: Gtk.Orientation.HORIZONTAL,
    bananagui.VERTICAL: Gtk.Orientation.VERTICAL,
}
_expand_indexes = {
    bananagui.HORIZONTAL: 0,
    bananagui.VERTICAL: 1,
}


class Box:

    def __init__(self, parent, **kwargs):
        gtk_orientation = _gtk_orientations[self['orientation']]
        widget = Gtk.Box(orientation=gtk_orientation)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def _bananagui_box_append(self, child):
        # TODO: What if the widget is added and then its expandiness is
        # changed?
        expandindex = _expand_indexes[self['orientation']]
        expand = child['expand'][expandindex]
        self['real_widget'].pack_start(child['real_widget'], expand, expand, 0)
        child['real_widget'].show()

    def _bananagui_box_remove(self, child):
        self['real_widget'].remove(child['real_widget'])
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
"""BananaGUI GTK+ 3 base."""

# flake8: noqa

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GLib', '2.0')

try:
    gi.require_version('AppIndicator3', '0.1')
    HAS_APPINDICATOR = True
except ValueError:
    HAS_APPINDICATOR = False

from gi.repository import Gtk
GTK_VERSION = (Gtk.MAJOR_VERSION, Gtk.MINOR_VERSION, Gtk.MICRO_VERSION)

from .bases import Widget, Parent, Child
from .buttons import BaseButton, Button, ImageButton
from .canvas import Canvas
from .clipboard import set_clipboard_text, get_clipboard_text
from .containers import Bin, Box
from .dialogs import (Dialog, infodialog, warningdialog, errordialog,
                      colordialog, fontdialog)
from .labels import BaseLabel, Label, ImageLabel
from .mainloop import init, main, quit
from .misc import (Checkbox, Dummy, Separator, Spinner, Spinbox, Slider,
                   Progressbar, get_font_families)
from .textwidgets import TextBase, Entry, PlainTextView
from .timeouts import add_timeout
from .trayicon import TrayIcon
from .window import BaseWindow, Window
from gi.repository import Gtk


class BaseLabel:
    pass


class Label:

    def __init__(self, parent, **kwargs):
        self.real_widget.raw_set(Gtk.Label(justify=Gtk.Justification.CENTER))
        super().__init__(parent, **kwargs)

    def _bananagui_set_text(self, text):
        self['real_widget'].set_text(text)


class ImageLabel:

    def __init__(self, parent, **kwargs):
        raise NotImplementedError  # TODO
        super().__init__(parent, **kwargs)

    def _bananagui_set_path(self, path):
        ...
from gi.repository import GLib

loop = None


def init():
    # Gtk.main() cannot be interrupted with Ctrl+C.
    global loop
    loop = GLib.MainLoop()


def main():
    loop.run()


def quit():
    global loop
    loop.quit()
    loop = None
from gi.repository import Gtk

import bananagui
from bananagui import utils


class Checkbox:

    def __init__(self, parent, **kwargs):
        widget = Gtk.CheckButton()
        widget.connect('notify::active', self.__on_check)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def __on_check(self, real_widget, gparam):
        self.checked.raw_set(real_widget.get_active())

    def _bananagui_set_text(self, text):
        self['real_widget'].set_label(text)

    def _bananagui_set_checked(self, checked):
        self['real_widget'].set_active(checked)


class Dummy:

    def __init__(self, parent, **kwargs):
        self.real_widget.raw_set(Gtk.Label())
        super().__init__(parent, **kwargs)


_orientations = {
    bananagui.HORIZONTAL: Gtk.Orientation.HORIZONTAL,
    bananagui.VERTICAL: Gtk.Orientation.VERTICAL,
}


class Separator:

    def __init__(self, parent, **kwargs):
        gtk_orientation = _orientations[self['orientation']]
        widget = Gtk.Separator(orientation=gtk_orientation)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)


class Spinner:

    def __init__(self, parent, **kwargs):
        # We need to hide the spinner when it's not spinning. Rest of
        # BananaGUI calls real_widget.show() when the widget is added
        # somewhere, so we need to create a container for it and add the
        # real spinner inside it.
        self.__spinner = Gtk.Spinner()
        container = Gtk.Box()
        container.pack_start(self.__spinner, True, True, 0)
        self.real_widget.raw_set(container)
        super().__init__(parent, **kwargs)

    def _bananagui_set_spinning(self, spinning):
        if spinning:
            self.__spinner.show()
            self.__spinner.start()
        else:
            self.__spinner.hide()
            self.__spinner.stop()


class Spinbox:

    def __init__(self, parent, **kwargs):
        minimum = min(self['valuerange'])
        maximum = max(self['valuerange'])
        step = utils.rangestep(self['valuerange'])
        widget = Gtk.SpinButton.new_with_range(minimum, maximum, step)
        widget.connect('notify::value', self.__value_changed)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def __value_changed(self, widget, gparam):
        self.value.raw_set(int(widget.get_value()))

    def _bananagui_set_value(self, value):
        self['real_widget'].set_value(value)


class Slider:

    def __init__(self, parent, **kwargs):
        range_args = (min(self['valuerange']), max(self['valuerange']),
                      utils.rangestep(self['valuerange']))
        widget = Gtk.Scale.new_with_range(
            _orientations[self['orientation']], *range_args)
        widget.connect('value-changed', self.__value_changed)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def __value_changed(self, widget):
        # TODO: something's wrong, the guitest prints hi a lot because
        # the value is set constantly when the scale is moved.
        value = int(widget.get_value())
        if value in self['valuerange']:
            self.value.raw_set(value)
        else:
            # TODO: is there a better way to allow only values in the
            # range?
            difference = value - self['value']
            if abs(difference) < utils.rangestep(self['valuerange'])/2:
                # Keeping the value where it is now is probably closest
                # to what the user wants.
                widget.set_value(self['value'])
            else:
                # Time to move the widget.
                if difference > 0:
                    # Let's move the scale up.
                    self['value'] += utils.rangestep(self['valuerange'])
                else:
                    # Let's move it down.
                    self['value'] -= utils.rangestep(self['valuerange'])
            widget.set_value(self['value'])

    def _bananagui_set_value(self, value):
        self['real_widget'].set_value(value)


class Progressbar:

    def __init__(self, parent, **kwargs):
        self.real_widget.raw_set(Gtk.ProgressBar())
        super().__init__(parent, **kwargs)

    def _bananagui_set_progress(self, progress):
        self['real_widget'].set_fraction(progress)


def get_font_families():
    # Based on http://zetcode.com/gui/pygtk/pango/
    widget = Gtk.Label()
    context = widget.create_pango_context()
    return (family.get_name() for family in context.list_families())
from gi.repository import Gtk


class TextBase:
    pass


class Entry:

    def __init__(self, parent, **kwargs):
        widget = Gtk.Entry()
        widget.connect('changed', self.__changed)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def __changed(self, entry):
        self.text.raw_set(entry.get_text())

    def _bananagui_set_text(self, text):
        self['real_widget'].set_text(text)

    def _bananagui_set_read_only(self, read_only):
        self['real_widget'].set_editable(not read_only)

    def select_all(self):
        self['real_widget'].select_region(0, -1)
        self['real_widget'].grab_focus()


class PlainTextView:
    # TODO: tabchar

    def __init__(self, parent, **kwargs):
        widget = Gtk.TextView()
        self.__buf = widget.get_buffer()
        self.__buf.connect('changed', self.__changed)
        self.real_widget.raw_set(widget)
        super().__init__(parent, **kwargs)

    def __changed(self, buf):
        self.text.raw_set(buf.get_text(buf.get_start_iter(),
                                       buf.get_end_iter(), True))

    def __bounds(self):
        return self.__buf.get_start_iter(), self.__buf.get_end_iter()

    def select_all(self):
        self.__buf.select_range(self.__buf.get_start_iter(),
                                self.__buf.get_end_iter())
        self['real_widget'].grab_focus()

    def clear(self):
        self.__buf.delete(self.__buf.get_start_iter(),
                          self.__buf.get_end_iter())

    def append_text(self, text):
        self.__buf.insert(self.__buf.get_end_iter(), text)
from gi.repository import GLib

import bananagui


def add_timeout(milliseconds, callback):
    def real_callback():
        return callback() == bananagui.RUN_AGAIN

    GLib.timeout_add(milliseconds, real_callback)
import os
import warnings

from gi.repository import Gtk

from . import HAS_APPINDICATOR
if HAS_APPINDICATOR:
    # Everything in this module starts with "Indicator" so I think it's
    # fine to use a from import.
    from gi.repository.AppIndicator3 import (
        Indicator, IndicatorCategory, IndicatorStatus)


class TrayIcon:

    def __init__(self, **kwargs):
        if HAS_APPINDICATOR:
            # This is a bit bad. There's no good way to get the name of
            # the application, and we also don't know the icon yet so
            # we need to set that to a dummy value.
            widget = Indicator.new(
                'bananagui-application',
                'dummy-icon-name',
                IndicatorCategory.APPLICATION_STATUS,
            )
            widget.set_status(IndicatorStatus.ACTIVE)
            # We need to set a menu to show the indicator.
            widget.set_menu(Gtk.Menu())
        else:
            # Fall back to deprecated Gtk.StatusIcon.
            widget = Gtk.StatusIcon()
        self.real_widget.raw_set(widget)
        super().__init__(**kwargs)

    def _bananagui_set_iconpath(self, path):
        if HAS_APPINDICATOR:
            # This needs to be absolute path or AppIndicator3 thinks
            # it's an icon name.
            self['real_widget'].set_icon(os.path.abspath(path))
        else:
            self['real_widget'].set_from_file(path)

    def _bananagui_set_tooltip(self, tooltip):
        if HAS_APPINDICATOR:
            warnings.warn("AppIndicator3 doesn't support tooltips")
        else:
            self['real_widget'].set_tooltip_text(tooltip)
from gi.repository import Gtk


class BaseWindow:

    def __init__(self, **kwargs):
        window = self['real_widget']
        window.set_title(self['title'])
        window.connect('delete-event', self.__delete_event)
        window.show()
        super().__init__(**kwargs)

    def _bananagui_set_title(self, title):
        self['real_widget'].set_title(title)

    # TODO: resizable and size don't work correctly if resizable is
    # False but size is set.
    def _bananagui_set_resizable(self, resizable):
        self['real_widget'].set_resizable(resizable)

    def _bananagui_set_size(self, size):
        self['real_widget'].resize(*size)

    def _bananagui_set_minimum_size(self, size):
        if size is None:
            size = (-1, -1)
        self['real_widget'].set_size_request(*size)

    def _bananagui_set_showing(self, showing):
        if showing:
            self['real_widget'].show()
        else:
            self['real_widget'].hide()

    def __delete_event(self, widget, event):
        self.on_destroy.emit()
        return True  # Block GTK's delete-event handling.

    def wait(self):
        raise NotImplementedError  # TODO

    def destroy(self):
        self['real_widget'].destroy()


class Window:

    def __init__(self, **kwargs):
        self.real_widget.raw_set(Gtk.Window())
        super().__init__(**kwargs)
