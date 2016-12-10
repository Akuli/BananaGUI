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

import contextlib

import bananagui
from bananagui import mainloop, utils


class Widget:
    """A baseclass for all widgets.

    Initialization keyword arguments are set as attributes to the
    instance.

    Attributes:
      base          The real GUI toolkit widget that BananaGUI uses.
                    This exposes all methods that the GUI toolkit has.
      can_focus     True if focus() can be called.
                    Unlike most other attributes in BananaGUI, this
                    is a class attribute.
    """

    can_focus = False

    def __init__(self):
        if not hasattr(self, 'base'):
            # A subclass didn't override __init__ and define a
            # base.
            raise TypeError("cannot create instances of %r directly, "
                            "instantiate a subclass instead"
                            % type(self).__name__)
        if not mainloop._initialized:
            raise ValueError("cannot create widgets without initializing "
                             "the main loop")
        self._blocked = set()

    @contextlib.contextmanager
    def block(self, callback_attribute):
        """Prevent callbacks from running temporarily.

        Blocking is instance-specific.
        """
        assert isinstance(callback_attribute, str)

        # This is important, we don't rely on an assertion here.
        if callback_attribute in self._blocked:
            raise ValueError("cannot block %r twice" % (callback_attribute,))

        self._blocked.add(callback_attribute)
        try:
            yield
        finally:
            self._blocked.remove(callback_attribute)

    def run_callbacks(self, callback_attribute, *extra_args):
        """Run each callback in self.CALLBACK_ATTRIBUTE.

        This does nothing if the callback is blocked. The callbacks are
        ran with the widget and extra_args as arguments.
        """
        if callback_attribute not in self._blocked:
            for callback in getattr(self, callback_attribute):
                callback(self, *extra_args)

    def focus(self):
        """Give the keyboard focus to this widget.

        Focusing a window also brings it in front of other windows.
        It's recommended to first create the widgets and then focus
        one of them to make sure that the widget gets focused with
        all GUI toolkits.
        """
        cls = type(self)
        assert cls.can_focus, "cannot focus %r widgets" % cls.__name__
        self.base.focus()


class Parent(Widget):
    """A base class for widgets that contain other widgets."""


@utils.add_property('tooltip')
@utils.add_property('grayed_out')
@utils.add_property('expand')
class Child(Widget):
    """A base class for widgets that can be added to Parent widgets.

    Children take a positional parent argument on initialization.
    The parent cannot be changed afterwards.

    The expand attribute determines the directions that the widget
    expands in. It's (True, True) by default, so the widget expands
    in both directions. When multiple widgets are next to each other
    in a container, at least one of them should expand in the
    container's direction, like this:

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
    toolkits. You can use a Dummy widget to fill the empty space if
    needed:

        ,------------------------------------------------.
        |   non-   |   non-   |                          |
        |expanding |expanding |       Dummy widget       |
        |  widget  |  widget  |                          |
        `------------------------------------------------'

    Attributes:
      parent        The parent widget set on initialization.
      tooltip       The widget's tooltip text, or None for no tooltip.
                    None by default.
      grayed_out    True if the widget looks like it's disabled.
                    This can be used to tell the user that the widget
                    can't be used for some reason.
      expand        Two-tuple of horizontal and vertical expanding.
    """

    def __init__(self, parent, *, tooltip=None, grayed_out=False,
                 expand=(True, True)):
        assert isinstance(parent, Parent)
        self.parent = parent
        self._tooltip = None
        self._grayed_out = False
        self._expand = (True, True)
        super().__init__()
        self.tooltip = tooltip
        self.grayed_out = grayed_out
        self.expand = expand

    def _check_tooltip(self, tooltip):
        assert tooltip is None or isinstance(tooltip, str)

    def _check_grayed_out(self, grayed_out):
        assert isinstance(grayed_out, bool)

    def _check_expand(self, expand):
        x, y = expand
        assert isinstance(x, bool) and isinstance(y, bool)


class _Oriented:
    """Implement an orientation attribute and handy class methods.

    There are many ways to create instances of _Oriented subclasses. For
    example, all of these do the same thing:

        SomeWidget(..., orientation=bananagui.HORIZONTAL)
        SomeWidget(..., orientation='h')
        SomeWidget.horizontal(...)

    Attributes:
      orientation       The orientation set on initialization.
    """

    # Subclasses should define self.orientation from a keyword-only
    # orientation argument.
    def __init__(self, *args, **kwargs):
        assert self.orientation in {bananagui.HORIZONTAL, bananagui.VERTICAL}
        super().__init__(*args, **kwargs)

    @classmethod
    def horizontal(cls, *args, **kwargs):
        """Create and return a new horizontal instance."""
        return cls(*args, orientation=bananagui.HORIZONTAL, **kwargs)

    @classmethod
    def vertical(cls, *args, **kwargs):
        """Create and return a new vertical instance"""
        return cls(*args, orientation=bananagui.VERTICAL, **kwargs)
