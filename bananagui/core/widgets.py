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

"""Baseclasses for the wrappers."""

import bananagui.core
from bananagui.utils import descriptors


class Widget(bananagui.core.BaseObject):
    """A widget baseclass.

    Properties:
        real_widget     R
            The real GUI toolkit widget that's being wrapped.
        tooltip         RW
            The widget's tooltip text. None by default.
    """

    properties = ['real_widget', 'tooltip']

    __tooltip = descriptors.StringOrNone(default=None)

    def get_real_widget(self):
        """Get the real GUI toolkit widget that is being wrapped."""
        raise NotImplementedError("override this")

    def set_tooltip(self, tooltip):
        """Set the tooltip."""
        self.__tooltip = tooltip
        self.tooltip.emit_changed()

    def get_tooltip(self):
        """Get the tooltip."""
        return self.__tooltip


_WidgetDescriptor = descriptors.IsInstance.from_type(Widget)
_WidgetOrNoneDescriptor = descriptors.IsInstance.from_type(
    Widget, or_none=True)


class Bin(Widget):
    """A widget that contains one child widget or no children at all.

    Properties:
        child           RW
            The only child or None. None by default.
            Setting this to None removes the child.
    """

    properties = ['child']
    __child = _WidgetOrNoneDescriptor(default=None)

    def set_child(self, child):
        """Set the child of the widget.

        If child is None, remove the existing child.
        """
        if child is not None:
            if not isinstance(child, Child):
                raise TypeError("%r is not a Child" % (child,))
            if child.get_parent() is not self:
                raise ValueError("cannot add a child with the wrong parent")
        self.__child = child
        self.child.emit_changed()

    def get_child(self):
        """Return the current child or None."""
        return self.__child


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

    Signals:
        on_close()
            The window is closed.
    """

    # TODO:
    #   - A property called "resizable", True by default.
    #   - A window icon property.

    properties = ['parentwindow', 'title', 'size', 'width', 'height']
    signals = ['on_close']

    __parentwindow = _WidgetOrNoneDescriptor()
    __title = descriptors.String(default="Window")
    __size = descriptors.Tuple(types=(int, int), default=(200, 200))

    def __init__(self, parentwindow=None):
        """Initialize the window."""
        self.__parentwindow = parentwindow
        super().__init__()

    def get_parentwindow(self):
        """Get the parent window set on initialization."""
        return self.__parentwindow

    def set_title(self, title):
        """Set the title."""
        self.__title = title
        self.title.emit_changed()

    def get_title(self):
        """Get the title."""
        return self.__title

    def set_size(self, size):
        """Set the size."""
        # This class keeps the size in a non-public instance variable,
        # and classes inherited from this class should call this method
        # every time the window is resized.
        self.__size = size
        self.size.emit_changed()

    def get_size(self):
        """Get the size."""
        return self.__size

    # Width and height for convinience.
    # Don't override these in a subclass.
    def set_width(self, width):
        height = self.get_height()
        self.set_size((width, height))

    def get_width(self):
        width, height = self.get_size()
        return width

    def set_height(self, height):
        width = self.get_width()
        self.set_size((width, height))

    def get_height(self):
        width, height = self.get_size()
        return height


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

    properties = ['parent', 'grayed_out']

    __grayed_out = descriptors.Boolean(default=False)

    def __init__(self, parent):
        """Initialize the child and set parent as its parent.

        The parent cannot be changed afterwards.
        """
        super().__init__()
        self.__parent = parent

    def get_parent(self):
        """Get the parent."""
        return self.__parent

    def set_grayed_out(self, grayed_out):
        """Gray out the widget or make it not grayed out."""
        self.__grayed_out = grayed_out
        self.grayed_out.emit_changed()

    def get_grayed_out(self):
        """Check if the widget is grayed out."""
        return self.__grayed_out


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

    properties = ['children', 'orientation']

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
