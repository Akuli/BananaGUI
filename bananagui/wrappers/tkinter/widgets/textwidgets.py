import tkinter as tk

from .basewidgets import Child, run_when_ready


def _setup_bindings(bananawidget, tkinterwidget):
    def callback(event):
        bananawidget.select_all()
        return 'break'

    tkinterwidget.bind('<Control-A>', callback)
    tkinterwidget.bind('<Control-a>', callback)


class Entry(Child):

    def create_widget(self, parent):
        self._var = tk.StringVar()
        self._var.trace('w', self._var_changed)
        widget = tk.Entry(parent.widget, textvariable=self._var)
        _setup_bindings(self.bananawidget, widget)
        return widget

    def _var_changed(self, tkname, empty_string, mode):
        self.bananawidget.text = self._var.get()

    @run_when_ready
    def set_text(self, text):
        self._var.set(text)

    # This overrides the set_grayed_out defined in basewidgets.py.
    @run_when_ready
    def set_grayed_out(self, grayed_out):
        self.widget['state'] = 'readonly' if grayed_out else 'normal'

    @run_when_ready
    def set_secret(self, secret):
        self.widget['show'] = '*' if secret else ''

    @run_when_ready
    def select_all(self):
        self.widget.selection_range(0, 'end')


class TextEdit(Child):

    def create_widget(self, parent):
        # A larger width or height would prevent the widget from
        # shrinking when needed.
        widget = tk.Text(parent.widget, width=1, height=1)
        widget.bind('<<Modified>>', self._on_modified)
        _setup_bindings(self.bananawidget, widget)
        return widget

    # TODO: the cursor likes to jump to the end of the widget and
    # "modified" prints too often...

    def _on_modified(self, event):
        print('modified')
        self.bananawidget.text = event.widget.get(0.0, 'end-1c')
        event.widget.edit_modified(False)

    @run_when_ready
    def set_text(self, text):
        print('setting text')
        self.widget.unbind('<<Modified>>')
        self.widget.delete(0.0, 'end-1c')
        self.widget.edit_modified(False)
        self.widget.bind('<<Modified>>', self._on_modified)
        self.widget.insert(0.0, text)

    @run_when_ready
    def set_grayed_out(self, grayed_out):
        self.widget['state'] = 'disable' if grayed_out else 'normal'

    @run_when_ready
    def select_all(self):
        # The end-1c doesn't get what tkinter thinks of as the last
        # character, which is a hidden newline.
        self.widget.tag_add('sel', 0.0, 'end-1c')
