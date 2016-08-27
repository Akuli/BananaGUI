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

"""Base classes for GUI toolkit wrappers."""

from bananagui import core


# Module-level functions
# ~~~~~~~~~~~~~~~~~~~~~~

def init():
    """Initialize the GUI."""


def main():
    """Run the mainloop until quit() is called."""


def quit(*args):
    """Ignore positional arguments and quit the mainloop.

    Return an exit status, or None if the GUI toolkit does not
    support it.
    """


# Base classes
# ~~~~~~~~~~~~

class WidgetBase:
    """A widget baseclass.

    Properties:
        real_widget     R
            The real GUI toolkit widget that's being wrapped.
        tooltip         RW
            The widget's tooltip text. None by default.
    """

    BASES = (core.ObjectBase,)
    real_widget = core.Property('real_widget')
    tooltip = core.Property('tooltip', converter=str, allow_none=True,
                            default=None)


class ParentBase:
    """A widget that child widgets can use as their parent."""

    BASES = ('WidgetBase',)


class ChildBase:
    """A widget that can be added to a container.

    Children take a parent argument on initialization. The parent
    property can be used to retrieve it, but the parent cannot be
    changed afterwards.

    Properties:
        parent          R
            The parent of this widget.
        grayed_out      RW
            True if the widget is grayed out, False otherwise.
    """

    BASES = ('WidgetBase',)
    parent = core.Property('parent')
    grayed_out = core.Property('grayed_out', converter=bool, default=False)

    def __init__(self, parent):
        super().__init__()
        self.raw_set('parent', parent)


class BinBase:
    """A widget that contains one child widget or no children at all.

    Properties:
        child           RW
            The child in the widget, None by default.
            Setting this to None removes the child.
    """

    BASES = ('ParentBase',)
    child = core.Property('child', allow_none=True, default=None)

    def _bananagui_set_child(self, child):
        #if not isinstance(child, ChildBase):
        #    raise TypeError("expected a child, got %r" % (child,))
        if child is not None and child['parent'] is not self:
            raise ValueError("can't add a child with the wrong parent")


# Labels
# ~~~~~~

class LabelBase:
    """A label base widget."""

    BASES = ('ChildBase',)


class Label:

    """A label with text in it.

    Properties:
        text            RW
            The label's text. An empty string by default.
    """

    # TODO: Add fonts and colors.
    BASES = ('LabelBase',)
    text = core.Property('text', converter=str, default='')


# Buttons
# ~~~~~~~

class ButtonBase:
    """A widget that can be pressed.

    Signals:
        on_click
            The button is clicked.
    """

    BASES = ('ChildBase',)
    on_click = core.Signal('on_click')


class Button:
    """A button with text.

    Properties:
        text            RW
            Text in the button. This is an empty string by default.
    """

    # TODO: Add fonts and colors.
    BASES = ('ButtonBase',)
    text = core.Property('text', converter=str, default='')


# Checkbox
# ~~~~~~~~

class Checkbox:
    """A widget that can be checked.

    Add a checkbox and a label into a HBox to create a checkbox with a
    label.

    Properties:
        checked         RWC
            True if the box is currently checked, False if not.
        text            RW
            The text next to the checkbox.
    """
    # TODO: colors & fonts

    BASES = ('ChildBase',)
    text = core.Property('text', converter=str, default='')
    checked = core.Property('checked', converter=bool, default=False)


# Text widgets
# ~~~~~~~~~~~~

class TextBase:
    """A base class for Entry and TextView.

    Properties:
        text            RWC
            The text in the entry.
    """

    # TODO: Add fonts and colors.
    BASES = ('ChildBase',)
    text = core.Property('text', converter=str, default='')


class Entry:
    """A one-line text widget.

    Properties:
        hidden          RW
            True if the entry's content is hidden with asterisks or balls.
            False by default.
    """

    BASES = ('TextBase',)
    hidden = core.Property('hidden', converter=bool, default=False)


class PlainTextView(io.TextIOBase):
    """A multiline text widget.

    An easy way to write to a text widget is to use it as a target file
    when printing:

        print("Hello!", file=some_textview)

    You can use the text property to get the current text.
    """

    BASES = ('TextBase',)

    def _bananagui_set_text(self, text):
        # Don't overwrite this in a GUI toolkit.
        self.clear()
        if text:
            self.write(text)

    def write(self, text):
        """Add text to the end of what is already in the text widget."""
        # Override this in a GUI toolkit, and be sure to do a
        # `return super().write(text)` at the end of the override.
        self.raw_set('text', self['text'] + text)
        return len(text)

    def clear(self):
        """Remove everything from the textview."""
        # Override this in GUI toolkits, and call this with super().
        self.raw_set('text', '')


# Layout widgets
# ~~~~~~~~~~~~~~

# TODO: Add a grid widget and a LayoutBase class.

class BoxBase:
    """A widget that contains other widgets in a row.

    Properties:
        children        RC
            A tuple of children in this widget.
            Modify this with the prepend, append an remove methods.
    """

    BASES = ('ParentBase', 'ChildBase')
    children = core.Property('children', converter=tuple, default=())

    def add_start(self, child, expand=False):
        """Start to add widgets from the beginning.

        If other widgets have been add_started, add this widget towards
        the center from them instead of pushing this widget all the way
        to the edge.
        """
        if child['parent'] is not self:
            raise ValueError("cannot prepend a child with the wrong parent")
        self.raw_set('children', (child,) + self['children'])

    def add_end(self, child, expand=False):
        """Add a widget to the end."""
        if child['parent'] is not self:
            raise ValueError("cannot append a child with the wrong parent")
        self.raw_set('children', self['children'] + (child,))

    def remove(self, child):
        """Remove a widget from self."""
        children = list(self['children'])
        children.remove(child)
        self.raw_set('children', tuple(children))

    def clear(self):
        """Remove all widgets from self."""
        self.raw_set('children', ())


class HBox:
    """A horizontal box."""

    BASES = ('BoxBase',)


class VBox:
    """A vertical box."""

    BASES = ('BoxBase',)


# Window classes
# ~~~~~~~~~~~~~~

def _convert2size(value):
    width, height = map(int, value)
    if width < 0 or height < 0:
        raise ValueError("width and height must be non-negative")
    return width, height


class WindowBase:
    """A window baseclass.

    The windows have a destroy() method, and it should be called when
    you don't need the window anymore. The windows can also be used as
    context managers, and the destroying will be done automatically:

        with ParentWindow() as my_window:
            ...

    Properties:
        title           RW
            The title of the window. 'Window' by default.
        resizable       RW
            True if the window can be resized, False otherwise.
        size            RWC
            Two-tuple of the width and height of the window.
            (200, 200) by default.
        minimum_size    RW
            The minimum size, or None.
            Like size, this is a two-tuple of width and height. The
            window cannot be resized to be smaller than this.
        maximum_size    RW
            The maximum size, or None.
            The window cannot be resized to be bigger than this.
        destroyed       RC
            True if the widget has been destroyed, False if not.
            You can destroy a window with the destroy method or by using
            the window as a context manager.
    """

    BASES = ('BinBase',)
    title = core.Property('title', converter=str, default="BananaGUI Window")
    resizable = core.Property('resizable', converter=bool, default=True)
    showing = core.Property('showing', converter=bool, default=False)
    size = core.Property('size', converter=_convert2size, default=(200, 200))
    minimum_size = core.Property('minimum_size', converter=_convert2size,
                                 default=None, allow_none=True)
    maximum_size = core.Property('maximum_size', converter=_convert2size,
                                 default=None, allow_none=True)
    minsize = minimum_size
    maxsize = maximum_size
    destroyed = core.Property('destroyed', converter=bool, default=False)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.destroy()

    def destroy(self):
        """Destroy the window."""
        self.raw_set('destroyed', True)


class Window:
    """A window that can have child windows.

    You can create multiple main windows.
    """

    BASES = ('WindowBase',)


class ChildWindow:
    """A window that has a parent window.

    On initialization, the window takes a parentwindow argument. This
    window may be centered over the parent window, it may be modal or
    whatever the real GUI toolkit supports.

    Properties:
        parentwindow    R
            A MainWindow instance.
    """

    BASES = ('BinBase',)
    parentwindow = core.Property('parentwindow')

    def __init__(self, parentwindow):
        super().__init__()
        self.raw_set('parentwindow', parentwindow)
