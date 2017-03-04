import tkinter as tk

from .basewidgets import Child, run_when_ready


class Slider(Child):

    def __init__(self, bananawidget, orient, valuerange):
        self._minimum = min(valuerange)
        self._maximum = max(valuerange)
        self._step = valuerange.step
        self._orient = orient.name.lower()
        super().__init__(bananawidget)

    def create_widget(self, parent):
        # The command is way better than binding anything manually. I
        # found it from the scale(3tk) man page.
        return tk.Scale(parent.widget, from_=self._minimum,
                        to=self._maximum, resolution=self._step,
                        orient=self._orient, command=self._do_changed)

    def _do_changed(self, new_value):
        self.bananawidget.value = int(new_value)

    @run_when_ready
    def set_value(self, value):
        self.widget.set(value)


def _select_all(event):
    try:
        # Tkinter's spinboxes don't have a selection_range method for
        # some reason, but entries have it.
        event.widget.selection('range', 0, 'end')
    except tk.TclError:
        # Maybe selection_range doesn't work with spinboxes on old Tk
        # versions?
        pass


class Spinbox(Child):

    def __init__(self, bananawidget, valuerange):
        self._valuerange = valuerange
        self._var = tk.StringVar(value=str(min(valuerange)))
        self._var.trace('w', self._var_changed)
        super().__init__(bananawidget)

    def create_widget(self, parent):
        widget = tk.Spinbox(
            parent.widget,
            # Tkinter doesn't know how to handle ranges.
            values=tuple(self._valuerange))
        widget.bind('<Control-A>', _select_all)
        widget.bind('<Control-a>', _select_all)
        widget['textvariable'] = self._var
        return widget

    def _var_changed(self, tkname, empty_string, mode):
        try:
            value = int(self._var.get())
            if value not in self.bananawidget.valuerange:
                return
        except ValueError:
            return
        self.bananawidget.value = value

    @run_when_ready
    def set_value(self, value):
        # This tells tkinter to call self._tkinter_var_changed and the
        # callbacks are ran.
        self._var.set(str(value))
