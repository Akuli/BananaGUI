from gi.repository import Gtk

from bananagui import utils
from . import orientations


class Slider:

    def __init__(self, parent, **kwargs):
        range_args = (min(self['valuerange']), max(self['valuerange']),
                      utils.rangestep(self['valuerange']))
        widget = Gtk.Scale.new_with_range(
            orientations[self['orientation']], *range_args)
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
