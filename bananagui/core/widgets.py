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

"""Define baseclasses for the wrappers."""

from bananagui import core


class Widget(core.BaseObject):
    """A widget baseclass.

    There is no .destroy() method. The widgets are automatically
    destroyed when they are not needed anymore.

    Properties:
        real_widget     R
            The real GUI toolkit widget that's being wrapped.
        tooltip         RW
            The widget's tooltip text or None.
    """

    def __init__(self):
        """Initialize the widget."""
        super().__init__()
        self.props['real_widget'] = core.Property(None)
        self.props['tooltip'] = core.Property(None)

    def __del__(self):
        """Destroy the widget to free up any resources used by it."""


class Bin(Widget):
    """A widget that contains one child widget or no children at all.

    Properties:
        child           RW
            The only child or None.
            Setting this to None removes the child.
    """

    def __init__(self):
        """Initialize the bin."""
        super().__init__()
        self.props['child'] = core.Property(None)


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
            The title of the window.
        showing         RW
            False if the window is hidden, True if not.
            Setting this to True also unminimizes the window.
        width           RW
            The width of the widget.
        height          RW
            The height of the widget.
        size            RW
            A two-tuple of width and height.
    """

    def __init__(self, parentwindow=None):
        """Initialize the window."""
        if parentwindow is not None and not isinstance(parentwindow, Window):
            raise TypeError("parentwindow must be a Window or None")
        super().__init__()
        self.props['parentwindow'] = core.Property(parentwindow)
        self.props['title'] = core.Property('Window')
        self.props['showing'] = core.Property(True)
        self.props['width'] = core.Property(200)
        self.props['width'].setter = self.__set_width
        self.props['width'].getter = self.__get_width
        self.props['height'] = core.Property(200)
        self.props['height'].setter = self.__set_height
        self.props['height'].getter = self.__get_height
        self.props['size'] = core.Property((200, 200))
        self.props['size'].setter = self.__set_size
        self.props['size'].getter = self.__get_size

    # These conflict with each other, but GUI implementations are
    # supposed to override some of these.
    def __set_width(self, width):
        self['size'] = width, self['height']

    def __get_width(self):
        width, height = self['size']
        return width

    def __set_height(self, height):
        self['size'] = self['width'], height

    def __get_height(self):
        width, height = self['size']
        return height

    def __set_size(self, size):
        self['width'], self['height'] = size

    def __get_size(self):
        return self['width'], self['height']


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

    def __init__(self, parent):
        """Initialize the child and set parent as its parent.

        The parent cannot be changed afterwards.
        """
        super().__init__()
        self.props['parent'] = core.Property(parent)
        self.props['grayed_out'] = core.Property(False)


class Box(Child):
    """A widget that contains other widgets in a horizontal or vertical row.

    Properties:
        children            R
            A tuple of children in this widget.
            Modify this with the prepend, append an remove methods. The
            getter returns a copy of the actual list.
        orientation         R
            This is set as a second positional (or keyword) argument on
            initialization. It can be 'horizontal' or 'vertical'.
    """

    def __init__(self, parent, orientation):
        """Initialize the box.

        In most cases, it's convenient to use hbox() or vbox() instead.
        """
        if orientation not in ('horizontal', 'vertical'):
            raise ValueError("unknown orientation {!r}".format(orientation))
        super().__init__(parent)
        self.props['children'] = core.Property([])
        self.props['children'].getter = self.__get_children
        self.props['orientation'] = core.Property(orientation)

    @classmethod
    def hbox(cls, parent):
        """Equivalent to cls(parent, 'horizontal')."""
        return cls(parent, 'horizontal')

    @classmethod
    def vbox(cls, parent):
        """Equivalent to cls(parent, 'vertical')."""
        return cls(parent, 'vertical')

    def __get_children(self):
        return self.props['children'].value.copy()

    def prepend(self, child, expand=False):
        """Add a widget to the beginning."""
        if child['parent'] is not self:
            raise ValueError("cannot prepend a child with the wrong parent")
        with self.props['children'].run_callbacks():
            self.props['children'].value.insert(0, child)

    def append(self, child, expand=False):
        """Add a widget to the end."""
        if child['parent'] is not self:
            raise ValueError("cannot append a child with the wrong parent")
        with self.props['children'].run_callbacks():
            self.props['children'].value.append(child)

    def remove(self, child):
        """Remove a widget from self."""
        with self.props['children'].run_callbacks():
            self.props['children'].value.remove(child)

    def clear(self):
        """Remove all widgets from self."""
        with self.props['children'].run_callbacks():
            self.props['children'].value.clear()


class Label(Child):
    """A label.

    Properties:
        text            RW
            The label's text.
    """

    def __init__(self, parent):
        """Initialize the label."""
        super().__init__(parent)
        self.props['text'] = core.Property('')


class ButtonBase(Child, Bin):
    """A widget that can be pressed.

    Properties:
        pressed         RW
            True if the button is pressed down, False if not.
    """

    def __init__(self, parent):
        """Initialize the button."""
        super().__init__(parent)
        self.props['pressed'] = core.Property(False)


class TextButton(ButtonBase):
    """A button with text.

    Properties:
        text            RW
            Text in the button or None.
    """

    def __init__(self, parent):
        """Initialize the button."""
        super().__init__(parent)
        self.props['text'] = core.Property('')


def main():
    """Run the mainloop until quit() is called."""


def quit(*args):
    """Quit the mainloop, and ignore all positional arguments."""
