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

"""Base classes for various widgets."""

from bananagui import _base
if _base is None:      # noqa
    raise ImportError("call bananagui.load() before importing %s"  # noqa
                      % __name__)

import functools
from gettext import gettext as _
import warnings

import bananagui
from bananagui import defaults, utils
from bananagui.structures import CallbackList


# Base classes
# ~~~~~~~~~~~~

@utils.baseclass
@bananagui.bananadoc
class Widget(_base.Widget, bananagui.BananaObject):
    """A widget baseclass."""

    # The tooltip property is not implemented here. Parent widgets don't
    # need tooltips because they should be always filled with Dummy
    # widgets.
    real_widget = bananagui.Property(
        'real_widget', settable=False,
        doc="The real GUI toolkit's widget that BananaGUI uses.")


@utils.baseclass
@bananagui.bananadoc
class Parent(_base.Parent, Widget):
    """A widget that child widgets can use as their parent."""


@utils.baseclass
@bananagui.bananadoc
class Child(_base.Child, Widget):
    """A widget that can be added to a container.

    Children take a parent argument on initialization. The parent
    property can be used to retrieve it, but the parent cannot be
    changed afterwards.
    """

    parent = bananagui.Property('parent', type=Parent, settable=False,
                                doc="The parent set on initialization.")
    tooltip = bananagui.Property(
        'tooltip', type=str, allow_none=True, default=None,
        doc="""Text in the widget's tooltip.

        This is None if the widget doesn't have a tooltip.
        """)
    expand = bananagui.Property(
        'expand', how_many=2, type=bool, default=(True, True),
        doc="""Two-tuple of horizontal and vertical expanding.

        For example, (True, True) will make the widget expand in
        both directions.

        **Note:** When multiple widgets are next to each other in a
        container, at least one of them needs to expand in the
        container's direction. Like this:

            ,------------------------------------------------.
            |   non-   |                                     |
            |expanding |           expanding widget          |
            |  widget  |                                     |
            `------------------------------------------------'

        Not like this:

            ,------------------------------------------------.
            |   non-   |   non-   |                          |
            |expanding |expanding |       empty space        |
            |  widget  |  widget  |                          |
            `------------------------------------------------'

        This way the children will behave consistently with all GUI
        toolkits. You can use a Dummy widget to fill the empty
        space:

            ,------------------------------------------------.
            |   non-   |   non-   |                          |
            |expanding |expanding |       Dummy widget       |
            |  widget  |  widget  |                          |
            `------------------------------------------------'

        """)
    grayed_out = bananagui.Property(
        'grayed_out', type=bool, default=False,
        doc="True if the widget is grayed out, False otherwise.")

    def __init__(self, parent: Parent, **kwargs):
        self.parent.raw_set(parent)
        super().__init__(**kwargs)


@utils.baseclass
@bananagui.bananadoc
class Oriented:
    """Implement an orientation property and handy class methods.

    There are many ways to create instances of Oriented subclasses. For
    example, all of these are valid ways to create a horizontal widget:

        SomeWidget.horizontal(...)
        SomeWidget(..., orientation='h')
        SomeWidget(..., orientation=bananagui.HORIZONTAL)
    """

    orientation = bananagui.Property(
        'orientation', settable=False,
        doc="""This is bananagui.HORIZONTAL or bananagui.VERTICAL.

        This is set with the last positional argument on initialization
        and cannot be changed afterwards.
        """)

    def __init__(self, *args, orientation, **kwargs):
        assert orientation in {bananagui.HORIZONTAL, bananagui.VERTICAL}, \
            "unknown orientation %r" % (orientation,)
        self.orientation.raw_set(orientation)
        super().__init__(*args, **kwargs)

    @classmethod
    def horizontal(cls, *args, **kwargs):
        """Create and return a new horizontal instance."""
        return cls(*args, orientation=bananagui.HORIZONTAL, **kwargs)

    @classmethod
    def vertical(cls, *args, **kwargs):
        """Create and return a new vertical instance."""
        return cls(*args, orientation=bananagui.VERTICAL, **kwargs)


def _check_valuerange(range_object):
    """Check if a range is valid for Ranged."""
    assert len(range_object) >= 2, \
        "%r contains less than two values" % (range_object,)
    assert utils.rangestep(range_object) > 0, \
        "%r has a non-positive step" % (range_object,)


@utils.baseclass
@bananagui.bananadoc
class Ranged:
    """Implement valuerange and value BananaGUI properties."""
    valuerange = bananagui.Property(
        'valuerange', type=range, settable=False,
        doc="""A range of allowed values.

        This must be a Python range object.
        """)
    value = bananagui.Property(
        'value', type=int,
        doc="""The current value.

        This must be in the valuerange.
        """)

    def __init__(self, *args, valuerange: range = range(11), **kwargs):
        """Set the value and range properties."""
        # The range is set before calling _check_valuerange because
        # setting it checks the type and we get better error messages.
        self.valuerange.raw_set(valuerange)
        _check_valuerange(valuerange)
        self.value.raw_set(min(valuerange))
        super().__init__(*args, **kwargs)

    def _bananagui_set_value(self, value):
        """Check if the value is in the range."""
        assert value in self['valuerange'], \
            "%r is not in %r" % (value, self['valuerange'])
        super()._bananagui_set_value(value)


# Layout widgets
# ~~~~~~~~~~~~~~

# This is not a Child because Window and Dialog are based on this.
@utils.baseclass
@bananagui.bananadoc
class Bin(_base.Bin, Parent):
    """A widget that contains one child widget or no children at all."""

    child = bananagui.Property(
        'child', allow_none=True, default=None, type=bases.Child,
        doc="""The child in the widget, None by default.

        Setting this to None removes the child.
        """)

    def _bananagui_set_child(self, child):
        if child is not None:
            assert child['parent'] is self, \
                "cannot add a child with the wrong parent"
        super()._bananagui_set_child(child)


@bananagui.bananadoc
class Box(Oriented, _base.Box, Parent, Child):
    """A widget that contains other widgets.

    The children property behaves like a list and you can modify it to
    add widgets to the box or remove widgets from the box.
    """
    # The base should define a _bananagui_box_append method that adds a
    # child widget to the end of the box and a _bananagui_box_remove
    # method that removes a child widget from the box.

    children = bananagui.Property(
        'children', getdefault=CallbackList, settable=False,
        doc="A mutable sequence of children in the box.")

    def __init__(self, parent, **kwargs):
        self['children']._callbacks.append(self.__children_changed)
        super().__init__(parent, **kwargs)

    def __children_changed(self, old, new):
        assert len(new) == len(set(new)), \
            "cannot add the same child twice"

        # TODO: Maybe old and new have something else in common than the
        # beginning? Optimize this.
        common = utils.common_beginning(old, new)

        # These are called from super() so a subclass can have an
        # _append or _remove method and it's not going to conflict.
        for child in old[common:]:
            super()._bananagui_box_remove(child)
        for child in new[common:]:
            assert child['parent'] is self, \
                "cannot add a child with the wrong parent"
            super()._bananagui_box_append(child)


# Window classes
# ~~~~~~~~~~~~~~

@utils.baseclass
@bananagui.bananadoc
class BaseWindow(_base.BaseWindow, Bin):
    """A window baseclass.

    BananaGUI windows have a destroy() method, and it should be called
    when you don't need the window anymore. The windows can also be used
    as context managers, and the destroying will be done automatically:

        with Window() as my_window:
            ...
    """
    # There is no maximum_size because X doesn't support it. Tkinter
    # implements it on X, but it does that by moving the window with a
    # maximum size to the upper left corner when it's maximized.

    @staticmethod
    def destroy_callback(event: bananagui.Event) -> None:
        """Destroy event.widget."""
        event.widget.destroy()

    resizable = bananagui.Property(
        'resizable', type=bool, default=True,
        doc="True if the window can be resized.")
    size = bananagui.Property(
        'size', how_many=2, type=int, minimum=1, default=(200, 200),
        doc="Two-tuple of the window's current width and height.")
    minimum_size = bananagui.Property(
        'minimum_size', default=None, how_many=2, type=int, minimum=1,
        allow_none=True,
        doc="""Two-tuple of minimum width and height or None.

        The window cannot be resized to be smaller than this.
        """)
    showing = bananagui.Property(
        'showing', type=bool, default=True,
        doc="True if the window is visible.")
    on_destroy = bananagui.Signal(
        'on_destroy',
        doc="""This is emitted when the user tries to close the window.

        Unlike most other signals, this contains a callback by default.
        It's BaseWindow.destroy_callback and it calls self.destroy. You
        can remove it if you don't want the window to get destroyed when
        the user tries to close it. You can also call self.destroy()
        from other callbacks.
        """)

    def __init__(self, **kwargs):
        self['on_destroy'].append(self.destroy_callback)
        self.__destroyed = False
        super().__init__(**kwargs)

    @property
    def destroyed(self) -> bool:
        """True if the window has been destroyed.

        This is not a BananaGUI property because there's no need to
        attach callbacks to this and you can use the on_destroy signal
        instead.
        """
        return self.__destroyed

    def __enter__(self):
        """Return the window."""
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Destroy the window."""
        self.destroy()

    def wait(self) -> None:
        """Wait until the window is destroyed."""
        super().wait()

    def destroy(self) -> None:
        """Destroy the window and set self.destroyed to True.

        This method can be called multiple times and it will do nothing
        after the first call. It's not recommended to override this, use
        the on_destroy signal instead.
        """
        if not self.destroyed:
            super().destroy()
            self.__destroyed = True


@bananagui.bananadoc
class Window(_base.Window, BaseWindow):
    """A window that can have child windows.

    The windows don't have a parent window. You can create multiple
    windows like this.
    """

    title = bananagui.Property(
        'title', type=str, default="BananaGUI Window",
        doc="The title of the window.")


@bananagui.bananadoc
class Dialog(_base.Dialog, window.BaseWindow):
    """A window that has a parent window.

    This class takes a parentwindow argument on initialization. The
    parent window must be an instance of Window and it may be centered
    over the parent window, it may be modal or whatever the real GUI
    toolkit supports. It's None by default.
    """

    title = bananagui.Property('title', type=str, default="BananaGUI Dialog",
                               doc="The title of the window.")
    parentwindow = bananagui.Property(
        'parentwindow', type=window.Window, settable=False,
        doc="The parent window set on initialization.")

    def __init__(self, parentwindow: window.Window, **kwargs):
        self.parentwindow.raw_set(parentwindow)
        super().__init__(parentwindow, **kwargs)


def _messagedialog(function):
    """Return a new message dialog function."""
    # We need to modify the original function first because
    # functools.wraps overrides everything the wrapped function has.
    function.__annotations__ = {
        'parentwindow': window.Window, 'message': str, 'title': str,
        'buttons': utils.abc.Sequence, 'defaultbutton': str, 'return': str}
    if function.__doc__ is not None:
        # Not running with Python's optimizations.
        function.__doc__ += """

        The buttons argument should be a sequence of button texts that
        will be added to the dialog. It defaults to "OK" translated with
        gettext.gettext in a list.

        The button with `default` as its text will have keyboard focus
        by default, unless defaultbutton is None.

        The text argument is the text that will be shown in the dialog.
        If title is not given, the dialog's title will be the same as
        parentwindow's title.

        The dialog doesn't have an icon on some GUI toolkits. The text
        of the clicked button is returned, or None if the dialog is
        closed.
        """

    @functools.wraps(function)
    def result(parentwindow, message, *, title=None, buttons=None,
               defaultbutton=None):
        # TODO: add something to Widget to handle defaultbutton?
        if title is None:
            title = parentwindow['title']
        if buttons is None:
            buttons = [_("OK")]
        assert buttons, "at least one button is required"
        assert defaultbutton is None or defaultbutton in buttons
        return function(parentwindow, message, title, buttons, defaultbutton)

    return result


# TODO: move this to utils?
def _find_attribute(attribute, *objects):
    for obj in objects:
        try:
            return getattr(obj, attribute)
        except AttributeError:
            pass
    raise AttributeError("none of the objects have an attribute %r"
                         % attribute)

_infodialog = _find_attribute('infodialog', _base, defaults)
_warningdialog = _find_attribute('warningdialog', _base, defaults)
_errordialog = _find_attribute('errordialog', _base, defaults)
_questiondialog = _find_attribute('questiondialog', _base, defaults)
_fontdialog = _find_attribute('fontdialog', _base, defaults)


@_messagedialog
def infodialog(*args):
    """Display a dialog with an information icon."""
    return _infodialog(*args)


@_messagedialog
def warningdialog(*args):
    """Display a dialog with a warning icon."""
    return _warningdialog(*args)


@_messagedialog
def errordialog(*args):
    """Display a dialog with an error icon."""
    return _errordialog(*args)


@_messagedialog
def questiondialog(*args):
    """Display a dialog with the question icon."""
    return _questiondialog(*args)


def colordialog(parentwindow: window.Window, *, title: str = None,
                default: bananagui.Color = bananagui.BLACK) -> bananagui.Color:
    """Ask a color from the user.

    This returns the new color, or None if the user canceled the dialog.
    """
    if title is None:
        title = parentwindow['title']
    return _base.colordialog(parentwindow, default, title)


def fontdialog(parentwindow: window.Window, *, title: str = None,
               default: bananagui.Font = bananagui.Font()) -> bananagui.Font:
    """Ask a font from the user.

    This returns the new font, or None if the user canceled the dialog.
    """
    if title is None:
        title = parentwindow['title']
    return _fontdialog(parentwindow, default, title)


# Labels
# ~~~~~~

@utils.baseclass
@bananagui.bananadoc
class BaseLabel(_base.BaseLabel, bases.Child):
    """A label base class."""


@bananagui.bananadoc
class Label(_base.Label, BaseLabel):
    """A label with text in it.

    Currently the text is always centered.
    """
    # TODO: add an alignment thing? Currently the text in the labels is
    # always centered.
    # TODO: Add fonts and colors?
    text = bananagui.Property('text', type=str, default='',
                              doc="Text in the label.")


@bananagui.bananadoc
class ImageLabel(_base.ImageLabel, BaseLabel):
    """A label that contains an image."""
    imagepath = bananagui.Property.imagepath(
        'imagepath', doc="Path to an image that will be displayed.")


# Buttons
# ~~~~~~~

@utils.baseclass
@bananagui.bananadoc
class BaseButton(_base.BaseButton, bases.Child):
    """Base for other buttons."""

    on_click = bananagui.Signal(
        'on_click', doc="This is emitted when the button is clicked.")


@bananagui.bananadoc
class Button(_base.Button, BaseButton):
    """A button that displays text in it."""

    text = bananagui.Property('text', type=str, default='',
                              doc="The text in the button.")


@bananagui.bananadoc
class ImageButton(_base.ImageButton, BaseButton):
    """A button that displays an image."""
    imagepath = bananagui.Property.imagepath(
        'imagepath',
        doc="Path to the image that is displayed in the button.")


# Canvas widget
# ~~~~~~~~~~~~~

@bananagui.bananadoc
class Canvas(_base.Canvas, Child):
    """A canvas widget that you can draw things on.

    When drawing on the canvas, the coordinates can be less than zero or
    greater than the width of the canvas.
    """

    minimum_size = bananagui.Property(
        'minimum_size', how_many=2, type=int, minimum=0, default=(300, 200),
        doc="""Two-tuple of the minimum width and height of the canvas.

        The canvas is smaller than this only if the window is resized
        to something smaller than this.
        """)
    size = bananagui.Property(
        'size', how_many=2, type=int, minimum=0, default=(300, 200),
        settable=False,
        doc="""Two-tuple of the current width and height of the canvas.

        This is updated when the canvas gets resized. The value is
        undefined when the canvas isn't in a visible container.
        """)
    background = bananagui.Property(
        'background', type=bananagui.Color, default=bananagui.WHITE,
        doc="""The background color of the canvas.

        This is the color of the canvas before anything is drawn to it,
        and clearing the canvas fills it with this color.
        """)

    def draw_line(self, start: tuple, end: tuple, *, thickness: int = 1,
                  color: bananagui.Color = bananagui.BLACK) -> None:
        """Draw a line from start to end on the canvas.

        It doesn't matter which position is start and which position is
        end. This method does nothing if color is None.
        """
        assert thickness > 0, "non-positive thickness %r" % (thickness,)
        if color is not None:
            super().draw_line(start, end, thickness, color)

    def draw_polygon(self, *corners, fillcolor: bananagui.Color = None,
                     linecolor: bananagui.Color = bananagui.BLACK,
                     linethickness: int = 1) -> None:
        """Draw a polygon.

        linecolor and fillcolor can be None.
        """
        assert len(corners) > 2, "use draw_line"
        assert linethickness > 0, \
            "non-positive linethickness %r" % (linethickness,)
        if fillcolor is not None or linecolor is not None:
            super().draw_polygon(
                *corners, fillcolor=fillcolor,
                linecolor=linecolor, linethickness=linethickness)

    def draw_oval(self, center: tuple, xradius: int, yradius: int, *,
                  fillcolor: bananagui.Color = None,
                  linecolor: bananagui.Color = bananagui.BLACK,
                  linethickness: int = 1) -> None:
        """Draw an oval on the canvas.

        linecolor and fillcolor can be None.
        """
        assert xradius > 0, "non-positive xradius %r" % (xradius,)
        assert yradius > 0, "non-positive yradius %r" % (yradius,)
        assert linethickness > 0, \
            "non-positive line thickness %r" % (linethickness,)
        super().draw_oval(center, xradius, yradius, fillcolor,
                          linecolor, linethickness)

    def draw_circle(self, center: tuple, radius: int, **kwargs) -> None:
        """Draw a circle on the canvas by calling self.draw_oval()."""
        self.draw_oval(center, radius, radius, **kwargs)

    def fill(self, color: bananagui.Color) -> None:
        """Fill the canvas with a color."""
        width, height = self['size']
        self.draw_polygon((0, 0), (0, height), (width, height), (width, 0),
                          fillcolor=self['background'], linecolor=None)

    def clear(self) -> None:
        """Clear the canvas by filling it with its background."""
        self.fill(self['background'])


# Clipboard management
# ~~~~~~~~~~~~~~~~~~~~

def set_clipboard_text(text: str) -> None:
    """Set text to the clipboard."""
    _base.set_clipboard_text(text)


def get_clipboard_text() -> str:
    """Return the text that is currently on the clipboard."""
    return _base.get_clipboard_text()


try:
    _SpinnerBase = _base.Spinner
except AttributeError:
    # The base doesn't provide a spinner. We need to create one using
    # other widgets.
    from bananagui.bases.defaults import Spinner as _SpinnerBase

# TODO: A RadioButton, or _RadioButton and RadioButtonManager.


@bananagui.bananadoc
class Checkbox(_base.Checkbox, bases.Child):
    """A widget that can be checked.

    The Checkbox widget has nothing to do with the Box widget.
    """

    text = bananagui.Property(
        'text', type=str, default='',
        doc="The text next to the box that can be checked.")
    checked = bananagui.Property(
        'checked', type=bool, default=False,
        doc="True if the box is currently checked, False if not.")


@bananagui.bananadoc
class Dummy(_base.Dummy, bases.Child):
    """An empty widget.

    This is useful for creating layouts with empty space that must be
    filled with something.
    """


@bananagui.bananadoc
class Separator(bases.Oriented, _base.Separator, bases.Child):
    """A horizontal or vertical line."""

    def __init__(self, parent, **kwargs):
        # Make the separator expand by default.
        orientation = kwargs.get('orientation')
        if orientation == bananagui.HORIZONTAL:
            kwargs.setdefault('expand', (True, False))
        if orientation == bananagui.VERTICAL:
            kwargs.setdefault('expand', (False, True))
        super().__init__(parent, **kwargs)


class Spinner(_find_attribute('Spinner', _base, defaults), bases.Child):
    """A waiting spinner.

    The spinner doesn't spin by default. You can set the spinning
    property to True to make it spin.
    """

    spinning = bananagui.Property(
        'spinning', type=bool, default=False,
        doc="True if the widget is currently spinning, False if not.")


class Spinbox(bases.Ranged, _base.Spinbox, bases.Child):
    """A box for selecting a number with arrow buttons up and down."""


class Slider(bases.Oriented, bases.Ranged, _base.Slider, bases.Child):
    """A slider for selecting a number."""


class Progressbar(bases.Oriented, _base.Progressbar, bases.Child):
    """A progress bar widget."""

    progress = bananagui.Property(
        'progress', type=(float, int), minimum=0, maximum=1, default=0,
        doc="The progressbar's position.")


def get_font_families() -> list:
    """Return a list of all avaliable font families."""
    # This is converted to a set first to make sure that we don't get
    # any duplicates. The base function can return anything iterable.
    return sorted(set(_base.get_font_families()))


@utils.baseclass
@bananagui.bananadoc
class TextBase(_base.TextBase, bases.Child):
    """A base class for text editing widgets."""

    # TODO: Add fonts and colors.
    text = bananagui.Property('text', type=str, default='',
                              doc="Text in the entry.")
    read_only = bananagui.Property(
        'read_only', type=bool, default=False,
        doc="True if the content of the widget cannot be edited.")

    # This is overrided just to make sure it has a docstring.
    def select_all(self) -> None:
        """Select all text in the widget.

        This also gives the keyboard focus to the widget.
        """
        super().select_all()


@bananagui.bananadoc
class Entry(_base.Entry, TextBase):
    """A one-line text widget."""

    hidden = bananagui.Property(
        'hidden', type=bool, default=False,
        doc="True if the entry's content is hidden with asterisks or balls.")


# TODO: text wrapping.
@bananagui.bananadoc
class PlainTextView(_base.PlainTextView, TextBase):
    """A multiline text widget."""

    tab_inserts = bananagui.Property(
        'tab_inserts', type=str, default='\t',
        doc="The character(s) that will be inserted when tab is pressed.")

    def _bananagui_set_text(self, text):
        old_text = self['text']
        if old_text == text:
            return

        # The changed signal needs to be emitted once only.
        with self.text.changed.blocked():
            self.clear()
            if text:
                self.append_text(text)
        self.text.changed.emit(old_value=old_text, new_value=text)

    def clear(self) -> None:
        """Remove everything from the textview."""
        super().clear()
        # The GUI toolkit's callback will update the text property.

    def append_text(self, text: str) -> None:
        """Add text to the end of what is already in the text widget."""
        super().append_text(text)
        # The GUI toolkit's callback will update the text property.


def add_timeout(milliseconds: int, callback, *args, **kwargs) -> None:
    """Run callback(*args, **kwargs) after waiting.

    If the function returns RUN_AGAIN it will be called again after
    waiting again. Depending on the GUI toolkit, the timing may start
    when bananagui.main() is started or before it.

    The waiting time is not guaranteed to be exact, but it's good enough
    for most purposes. Use something like time.time() if you need to
    measure time in the callback function.
    """
    # TODO: in bases, generate a warning if the function returns
    # something else than None or RUN_AGAIN.
    assert milliseconds > 0, "non-positive timeout %r" % (milliseconds,)
    assert callable(callback), "non-callable callback"

    def real_callback():
        result = callback(*args, **kwargs)
        if result not in {None, bananagui.RUN_AGAIN}:
            warnings.warn("BananaGUI callback didn't return None or "
                          "RUN_AGAIN, the result will be treated as None",
                          RuntimeWarning)
            result = None
        return result

    _base.add_timeout(milliseconds, real_callback)


class TrayIcon(_base.TrayIcon, bases.Widget):
    """An application indicator that will be displayed in the system tray."""

    # TODO: the trayicon's size shouldn't be hard-coded.
    iconpath = bananagui.Property.imagepath(
        'iconpath', settable=False,
        doc="""A path to the icon that will be displayed in the system tray.

        The icon should be 22 pixels wide and 22 pixels high.
        """)
    tooltip = bananagui.Property(
        'tooltip', type=str, allow_none=True, default=None,
        doc="""The trayicon's tooltip.

        Note that the tooltip is not displayed on some platforms.
        """)
    # TODO: A menu property, but not an on_click property. This will be
    #       an indicator instead of a tray icon on some platforms.


# Main loop
# ~~~~~~~~~

_initialized = False
_running = False


def init():
    """Initialize bananagui.gui.

    This is called automatically when bananagui.gui is imported for the
    first time.
    """
    global _initialized
    if not _initialized:
        _base.init()
        _initialized = True


def main():
    """Run bananagui.gui's mainloop until quit() is called.

    Raise an exception on failure.
    """
    global _initialized
    global _running
    assert _initialized, "init() wasn't called before calling main()"
    assert not _running, "two mainloops cannot be running at the same time"
    _running = True
    try:
        _base.main()
    finally:
        _running = False
        _initialized = False


def quit(*args):
    """Stop the mainloop started by main().

    All positional arguments are ignored. Quitting when the main loop is
    not running does nothing.
    """
    if _running:
        _base.quit()


# Initialize the GUI so people don't need to call gui.init() after
# importing it.
init()
