"""Define baseclasses for the wrappers."""

from gui import core


class Widget:
    """A widget baseclass.

    There is no .destroy() method. The widgets are automatically
    destroyed when they are not needed anymore.

    Properties:
        real_widget     R
            The real GUI toolkit widget that's being wrapped.
        tooltip         RW
            The widget's tooltip text or None.
    """

    def __init__(self, **kwargs):
        """Initialize the widget.

        Keyword arguments are passed to self.config.
        """
        self.real_widget = core.Property(None)
        self.tooltip = core.Property(None)
        self.config(**kwargs)

    def config(self, **kwargs):
        """Configure properties from keyword arguments.

        This is much like config in tkinter.
        """
        for propname, value in kwargs.items():
            getattr(self, propname)(value)

    def __del__(self):
        """Destroy the widget to free up any resources used by it."""
        super().__del__()


class Bin(Widget):
    """A widget that contains one child widget or no children at all.

    Properties:
        child           RW
            The only child or None.
            Setting this to None removes the child.
    """

    def __init__(self, **kwargs):
        """Initialize the bin."""
        super().__init__()
        self.child = core.Property(None)
        self.config(**kwargs)


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

    def __init__(self, parentwindow=None, **kwargs):
        """Initialize the window."""
        if parentwindow is not None and not isinstance(parentwindow, Window):
            raise TypeError("parentwindow must be a Window")
        super().__init__()
        self.parentwindow = core.Property(parentwindow)
        self.title = core.Property('Window')
        self.showing = core.Property(True)
        self.width = core.Property(200)
        self.width._setter = self.__set_width
        self.width._getter = self.__get_width
        self.height = core.Property(200)
        self.height._setter = self.__set_height
        self.height._getter = self.__get_height
        self.size = core.Property((200, 200))
        self.size._setter = self.__set_size
        self.size._getter = self.__get_size

        # These were not passed to super().__init__() because the
        # properties weren't set up when it was ran.
        self.config(**kwargs)

    # These conflict with each other, but GUI implementations are
    # supposed to override some of these.
    def __set_width(self, width):
        size = width, self.height()
        self.size(size)

    def __get_width(self):
        width, height = self.size()
        return width

    def __set_height(self, height):
        size = self.width(), height
        self.size(size)

    def __get_height(self):
        width, height = self.size()
        return height

    def __set_size(self, size):
        width, height = size
        self.width(width)
        self.height(height)

    def __get_size(self):
        return self.width(), self.height()


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

    def __init__(self, parent, **kwargs):
        """Initialize the child and set parent as its parent.

        The parent cannot be changed afterwards.
        """
        super().__init__()
        self.parent = core.Property(parent)
        self.grayed_out = core.Property(False)
        self.config(**kwargs)


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

    def __init__(self, parent, orientation, **kwargs):
        """Initialize the box.

        In most cases, it's convenient to use hbox() or vbox() instead.
        """
        if orientation not in ('horizontal', 'vertical'):
            raise ValueError("unknown orientation {!r}".format(orientation))
        super().__init__(parent)
        self.children = core.Property([])
        self.children.getter = self.__get_children
        self.orientation = core.Property(orientation)
        self.config(**kwargs)

    @classmethod
    def hbox(cls, parent):
        """Equivalent to cls(parent, 'horizontal')."""
        return cls(parent, 'horizontal')

    @classmethod
    def vbox(cls, parent):
        """Equivalent to cls(parent, 'vertical')."""
        return cls(parent, 'vertical')

    def __get_children(self):
        return self.children._value.copy()

    def prepend(self, child, expand=False):
        """Add a widget to the beginning."""
        if child.parent() is not self:
            raise ValueError("cannot prepend a child with the wrong parent")
        with self.children._run_callbacks():
            self.children._value.insert(0, child)

    def append(self, child, expand=False):
        """Add a widget to the end."""
        if child.parent() is not self:
            raise ValueError("cannot append a child with the wrong parent")
        with self.children._run_callbacks():
            self.children._value.append(child)

    def remove(self, child):
        """Remove a widget from self."""
        with self.children._run_callbacks():
            self.children._value.remove(child)


class Label(Child):
    """A label.

    Properties:
        text            RW
            The label's text.
    """

    def __init__(self, parent):
        """Initialize the label."""
        super().__init__(parent)
        self.text = core.Property('')


class ButtonBase(Child, Bin):
    """A widget that can be pressed.

    Properties:
        pressed         RW
            True if the button is pressed down, False if not.
    """

    def __init__(self, parent):
        """Initialize the button."""
        super().__init__(parent)
        self.pressed = core.Property(False)


class TextButton(ButtonBase):
    """A button with text.

    Properties:
        text            RW
            Text in the button or None.
    """

    def __init__(self, parent):
        """Initialize the button."""
        super().__init__(parent)
        self.text = core.Property('')


def main():
    """Run the mainloop until quit() is called."""


def quit(*args):
    """Quit the mainloop, and ignore all positional arguments."""
