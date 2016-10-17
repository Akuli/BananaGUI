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


def get_font_families():
    # Based on http://zetcode.com/gui/pygtk/pango/
    widget = Gtk.Label()
    context = widget.create_pango_context()
    return (family.get_name() for family in context.list_families())
