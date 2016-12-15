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
from bananagui import mainloop, types


class Widget(types.BananaObject):
    """A baseclass for all widgets.

    Attributes:
      real_widget   The real GUI toolkit widget that BananaGUI uses.
      can_focus     True if focus() can be called.
                    Unlike most other attributes in BananaGUI, this
                    is a class attribute.
    """

    can_focus = False

    def __init__(self):
        if not mainloop._initialized:
            raise ValueError("cannot create widgets without initializing "
                             "the main loop")
        super().__init__()

    @property
    def real_widget(self):
        return self._base.real_widget

    def focus(self):
        """Give the keyboard focus to this widget.

        Focusing a window also brings it in front of other windows.
        It's recommended to first create the widgets and then focus
        one of them to make sure that the widget gets focused correctly
        with all GUI toolkits.
        """
        cls = type(self)
        assert cls.can_focus, "cannot focus %r widgets" % cls.__name__
        self._base.focus()


class Parent(Widget):
    """A base class for widgets that contain other widgets."""


@types.add_property('tooltip')
@types.add_property('grayed_out')
@types.add_property('expand')
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

    def _repr_parts(self):
        if self.tooltip is None:
            # No need to add anything.
            return super()._repr_parts()
        # The tooltip can help with distinguishing widgets.
        return ['tooltip=' + repr(self.tooltip)] + super()._repr_parts()

    def _check_tooltip(self, tooltip):
        assert tooltip is None or isinstance(tooltip, str)

    def _check_grayed_out(self, grayed_out):
        assert isinstance(grayed_out, bool)

    def _check_expand(self, expand):
        x, y = expand
        assert isinstance(x, bool) and isinstance(y, bool)


_orientation_names = {bananagui.HORIZONTAL: 'horizontal',
                      bananagui.VERTICAL: 'vertical'}


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

    def _repr_parts(self):
        name = _orientation_names[self.orientation]
        return [name] + super()._repr_parts()

    @classmethod
    def horizontal(cls, *args, **kwargs):
        """Create and return a new horizontal instance."""
        return cls(*args, orientation=bananagui.HORIZONTAL, **kwargs)

    @classmethod
    def vertical(cls, *args, **kwargs):
        """Create and return a new vertical instance"""
        return cls(*args, orientation=bananagui.VERTICAL, **kwargs)