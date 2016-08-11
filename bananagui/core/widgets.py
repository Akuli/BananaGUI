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

"""Baseclasses for the wrappers.

The wrappers are supposed to create most of the properties and signals.
"""

from bananagui.core import BaseObject, properties


class Widget(BaseObject):
    """A widget baseclass.

    Properties:
        real_widget     R
            The real GUI toolkit widget that's being wrapped or None.
        tooltip         RW
            The widget's tooltip text. None by default.
    """

    real_widget = properties.Anything(
        allow_none=True,
    )
    tooltip = properties.String(
        allow_none=True,
        get_default=lambda: None,
    )


class Bin(Widget):
    """A widget that contains one child widget or no children at all.

    Properties:
        child           RW
            The child in the widget, None by default.
            Setting this to None removes the child.
    """

    child = properties.IsInstance(
        required_type=Widget,
        allow_none=True,
        default=lambda: None,
    )


class Window(Bin):
    """A window.

    On initialization, the window takes a parentwindow argument. It's
    None by default. If it's a window, the window may be centered over
    the parent, it may be modal or whatever the real GUI toolkit
    supports. Note that this class is not inherited from Child, and
    defining a parentwindow doesn't make it a child of this window.

    Properties:
        parentwindow    R
            The parent window set on initialization.
        title           RW
            The title of the window. 'Window' by default.
        size            RWC
            A two-tuple of the window's width and height.
            This is (200, 200) by default. You can also use a list when
            setting the size.
        width           RW
        height          RW
            The first and second item of size for convenience.
        resizable       RW
            True if the window can be resized, False otherwise.

    Signals:
        on_close()
            The window is closed.
    """

    parentwindow = properties.Anything(
        allow_none=True,
    )
    title = properties.String(
        allow_none=False,
    )
    size = properties.Tuple(
        types=(int, int),
        convert=,
        allow_none=False,
    )


class Child(Widget):
    """A widget that can be added to a parent widget.

    Child widgets take a parent argument on initialization, and the
    widget will be created inside the parent. The parent property can be
    used to retrieve it, but it cannot be changed afterwards.

    Properties:
        parent          R
            The parent of this widget.
        grayed_out      RW
            True if the widget is grayed out, False otherwise.
    """


class Box(Child):
    """A widget that contains other widgets in a horizontal or vertical row.

    Properties:
        children            RC
            A list of children in this widget.
            Modify this with the prepend, append an remove methods. The
            getter returns a copy of the actual list.
        orientation         R
            This is set as a second positional (or keyword) argument on
            initialization. It can be constants.HORIZONTAL or
            constants.VERTICAL.
    """

    def __init__(self, parent, orientation):
        """Initialize the box.

        In most cases, it's convenient to use hbox() or vbox() instead.
        """
        if orientation not in (bananagui.HORIZONTAL, bananagui.VERTICAL):
            raise ValueError("unknown orientation {!r}".format(orientation))
        super().__init__(parent)
        self.__orientation = orientation
        self.__children = []  # This must be here in __init__.

    @classmethod
    def hbox(cls, parent):
        """Create a horizontal box.

        This is equivalent to cls(parent, bananagui.HORIZONTAL).
        """
        return cls(parent, bananagui.HORIZONTAL)

    @classmethod
    def vbox(cls, parent):
        """Create a vertical box.

        This is equivalent to cls(parent, bananagui.VERTICAL).
        """
        return cls(parent, bananagui.VERTICAL)

    def get_orientation(self):
        """Return the orientation set on initialization."""
        return self.__orientation

    def get_children(self):
        """Get the children."""
        return self.__children.copy()

    def prepend(self, child, expand=False):
        """Add a widget to the beginning."""
        if child['parent'] is not self:
            raise ValueError("cannot prepend a child with the wrong parent")
        self.__children.insert(0, child)
        self.children.emit_changed()

    def append(self, child, expand=False):
        """Add a widget to the end."""
        if child['parent'] is not self:
            raise ValueError("cannot append a child with the wrong parent")
        self.__children.append(child)
        self.children.emit_changed()

    def remove(self, child):
        """Remove a widget from self."""
        self.__children.remove(child)
        self.children.emit_changed()

    def clear(self):
        """Remove all widgets from self."""
        self.__children.clear()
        self.children.emit_changed()


class Label(Child):
    """A label.

    Properties:
        text            RW
            The label's text. An empty string by default.
    """

    properties = ['text']
    __text = ''

    def set_text(self, text):
        """Set the text in the label."""
        self.__text = text
        self.text.emit_changed()

    def get_text(self):
        """Get the text in the label."""
        return self.__text


class ButtonBase(Child):
    """A widget that can be pressed.

    Signals:
        on_click()
            The button is clicked.
    """

    signals = ['on_click']


class TextButton(ButtonBase):
    """A button with text.

    Properties:
        text            RW
            Text in the button. This is an empty string by default.
    """

    properties = ['text']
    __text = ''

    def set_text(self, text):
        """Set the button's text."""
        self.__text = text

    def get_text(self):
        """Get the button's text."""


def main():
    """Run the mainloop until quit() is called.

    Return an exit status if the wrapped GUI toolkit supports it.
    """


def quit():
    """Quit the mainloop."""
