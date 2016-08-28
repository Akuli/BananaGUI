# Copyright (c) 2016 Akuli

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

"""GTK+ 3.0 wrapper for BananaGUI."""

# TODO: Clipboard functions.

import gi
gi.require_version('Gtk', '3.0')  # noqa
from gi.repository import Gtk


# Module-level functions
# ~~~~~~~~~~~~~~~~~~~~~~

def init():
    pass


def main():
    Gtk.main()


def quit(*args):
    Gtk.main_quit()


# Base classes
# ~~~~~~~~~~~~

class ChildBase:

    def _bananagui_set_grayed_out(self, grayed_out):
        self['real_widget'].set_sensitive(not grayed_out)

    def _bananagui_set_tooltip(self, tooltip):
        self['real_widget'].set_tooltip_text(tooltip)


class BinBase:

    def _bananagui_set_child(self, child):
        super()._bananagui_set_child(child)
        if self['child'] is not None:
            self.remove(self['child']['real_widget'])
        if child is not None:
            self['real_widget'].add(child['real_widget'])


# Labels
# ~~~~~~

class Label:

    def __init__(self, parent):
        super().__init__(parent)
        self.raw_set('real_widget', Gtk.Label())

    def _bananagui_set_text(self, text):
        self['real_widget'].set_text(text)


# Buttons
# ~~~~~~~

class Button:

    def __init__(self, parent):
        super().__init__(parent)
        widget = Gtk.Button()
        widget.connect('clicked', self.__on_click)
        self.raw_set('real_widget', widget)

    def __on_click(self, button):
        self.emit('on_click')

    def _bananagui_set_text(self, text):
        self['real_widget'].set_label(text)


# Checkbox
# ~~~~~~~~

class Checkbox:

    def __init__(self, parent):
        super().__init__(parent)
        widget = Gtk.CheckButton()
        widget.connect('notify::active', self.__toggled)
        self.raw_set('real_widget', widget)

    def __toggled(self, checkbutton, gparam):
        self.raw_set('checked', checkbutton.get_active())

    def _bananagui_set_checked(self, checked):
        self['real_widget'].set_active(checked)

    def _bananagui_set_text(self, text):
        self['real_widget'].set_label(text)


# Text widgets
# ~~~~~~~~~~~~

class Entry:

    def __init__(self, parent):
        super().__init__(parent)

        widget = Gtk.Entry()
        widget.connect('changed', self.__changed)
        self.raw_set('real_widget', widget)

    def __changed(self, entry):
        self.raw_set('text', entry.get_text())

    def _bananagui_set_text(self, text):
        self['real_widget'].set_text(text)
        # Setting the text will emit the GTK+ changed signal, and the
        # BananaGUI text property will be updated.

    # TODO: maybe select_all() shouldn't be just a tkinter thing and
    #       other wrappers should also provide it?

    # TODO: BananaGUI property called editable. With that and
    #       select_all(), entries could be used for displaying text that
    #       that the user can highlight and copy-paste somewhere else.


class PlainTextView:
    # TODO: Selecting between spaces and tabs.
    # TODO: In base.py, setting the text first clears the widget and
    #       then sets the text. It should block the text.changed signal
    #       so that it's only emitted once.

    def __init__(self, parent):
        super().__init__(parent)

        widget = Gtk.TextView()
        self.__buf = widget.get_buffer()
        self.raw_set('real_widget', widget)

    def clear(self):
        self.__buf.delete(self.__buf.get_start_iter(),
                          self.__buf.get_end_iter(),
                          True)


# Layout widgets
# ~~~~~~~~~~~~~~


# Window classes
# ~~~~~~~~~~~~~~

class WindowBase:

    def __init__(self):
        super().__init__()
        self['real_widget'].connect('delete-event', self.__delete_event)
        self['real_widget'].set_title(self['title'])

    def __delete_event(self, window, event):
        self.destroy()

    def destroy(self):
        if self['destroyed']:
            return
        self['real_widget'].destroy()
        super().destroy()

    def _bananagui_set_title(self, title):
        self['real_widget'].set_title(title)

    # TODO: non-resizable windows with a custom size
    # http://stackoverflow.com/questions/3582558/setting-resizable-to-false-shrinks-window-to-point
    def _bananagui_set_resizable(self, resizable):
        self['real_widget'].set_resizable(False)

    def _bananagui_set_size(self, size):
#        old_resizable = self['resizable']
#        self['resizable'] = True
        self['real_widget'].resize(*size)
#        self['resizable'] = old_resizable

    def _bananagui_set_minimum_size(self, size):
        if size is None:
            # GTK+ uses (-1, -1) as the default size request.
            size = (-1, -1)
        self['real_widget'].set_size_request(*size)


class Window:

    def __init__(self):
        self.raw_set('real_widget', Gtk.Window())
        super().__init__()
