from gi.repository import Gtk

import bananagui


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
        raise NotImplementedError  # TODO


class Slider:

    def __init__(self, parent, **kwargs):
        raise NotImplementedError  # TODO


def get_font_families():
    # Based on http://zetcode.com/gui/pygtk/pango/
    widget = Gtk.Label()
    context = widget.create_pango_context()
    return (family.get_name() for family in context.list_families())
