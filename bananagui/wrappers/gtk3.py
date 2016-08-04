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

"""GTK+ 3 wrapper for BananaGUI."""

import functools

import gi
gi.require_version('Gtk', '3.0')    # noqa
from gi.repository import Gtk

from bananagui import constants
from bananagui.core import widgets


# All windows will be added here. They will be shown when the mainloop
# is started.
_windows = []


class Widget(widgets.Widget):

    __doc__ = widgets.Widget.__doc__

    @functools.wraps(widgets.Widget.__init__)
    def __init__(self):
        super().__init__()
        self.tooltip._setter = self.__set_tooltip

    def __set_tooltip(self, tooltip):
        self['real_widget'].set_tooltip_text(tooltip)

    # I had problems with implementing a __del__, and it seemed like the
    # widgets were already destroyed by the time __del__ was ran.


class Bin(widgets.Bin, Widget):

    __doc__ = widgets.Bin.__doc__

    @functools.wraps(widgets.Bin.__init__)
    def __init__(self):
        super().__init__()
        self.child._setter = self.__set_child

    def __set_child(self, child):
        # Check if the child is already in the bin.
        if child is self['child']:
            return

        # Remove the old child if it's set.
        if self['child'] is not None:
            self['real_widget'].remove(self['child']['real_widget'])

        # Check the new child and add it.
        if child is not None:
            if child['parent'] is not self:
                raise ValueError("cannot add a child with the wrong parent")
            self['real_widget'].add(child['real_widget'])

        # Change the property's value.
        self.child._value = child
        self.child.emit_changed()


class Window(widgets.Window, Bin):

    __doc__ = widgets.Bin.__doc__

    @functools.wraps(widgets.Window.__init__)
    def __init__(self, parentwindow=None):
        super().__init__(parentwindow=parentwindow)
        _windows.append(self)
        self.real_widget._value = Gtk.Window(title=self['title'])
        if parentwindow is not None:
            self['real_widget'].set_transient_for(parentwindow['real_widget'])
        self['real_widget'].connect('delete-event', self.__on_delete_event)
        self.title._setter = self['real_widget'].set_title
        self.size._setter = self.__set_size
        self.size._getter = self['real_widget'].get_size

    def __on_delete_event(self, window, event):
        self.on_close.emit()

    def __set_size(self, size):
        self['real_widget'].resize(*size)


class Child(widgets.Child, Widget):

    __doc__ = widgets.Child.__doc__

    @functools.wraps(widgets.Child.__init__)
    def __init__(self, parent):
        super().__init__(parent)
        self.grayed_out._setter = self.__set_grayed_out

    def __set_grayed_out(self, grayed_out):
        self['real_widget'].set_sensitive(not grayed_out)


class Box(widgets.Box, Child):

    __doc__ = widgets.Child.__doc__

    @functools.wraps(widgets.Box.__init__)
    def __init__(self, parent, orientation):
        super().__init__(parent, orientation)
        orientations = {
            constants.HORIZONTAL: Gtk.Orientation.HORIZONTAL,
            constants.VERTICAL: Gtk.Orientation.VERTICAL,
        }
        self.real_widget._value = Gtk.Box(
            orientation=orientations[orientation])

    @functools.wraps(widgets.Box.prepend)
    def prepend(self, child, expand=False):
        super().prepend(child, expand=expand)
        # For some reason, calling pack_end adds the widget to top or
        # left.
        self['real_widget'].pack_end(child['real_widget'], expand, expand, 0)

    @functools.wraps(widgets.Box.append)
    def append(self, child, expand=False):
        super().append(child, expand=expand)
        self['real_widget'].pack_start(child['real_widget'], expand, expand, 0)

    @functools.wraps(widgets.Box.remove)
    def remove(self, child):
        super().remove(child)
        self['real_widget'].remove(child['real_widget'])


class Label(widgets.Label, Child):

    __doc__ = widgets.Label.__doc__

    @functools.wraps(widgets.Label.__init__)
    def __init__(self, parent):
        super().__init__(parent)
        self.real_widget._value = Gtk.Label(self['parent']['real_widget'])
        self.text._setter = self['real_widget'].set_text


class ButtonBase(widgets.ButtonBase, Child):

    __doc__ = widgets.ButtonBase.__doc__


class TextButton(widgets.TextButton, ButtonBase):

    __doc__ = widgets.ButtonBase.__doc__

    def __init__(self, parent):
        super().__init__(parent)
        self.real_widget._value = Gtk.Button()
        self['real_widget'].connect('clicked', self.__on_click)
        self.text._setter = self['real_widget'].set_label

    def __on_click(self, widget):
        self.on_click.emit()


@functools.wraps(widgets.main)
def main():
    for window in _windows:
        window['real_widget'].show_all()
    Gtk.main()
    _windows.clear()


@functools.wraps(widgets.quit)
def quit():
    Gtk.main_quit()
