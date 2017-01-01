# Copyright (c) 2016-2017 Akuli

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

import bananagui
from bananagui import images, mainloop, types


class Widget:
    """A baseclass for all widgets.

    Attributes:
      real_widget   The real GUI toolkit widget that BananaGUI uses.
      can_focus     True if focus() can be called.
                    Unlike most other attributes in BananaGUI, this
                    is a class attribute.
    """

    can_focus = False

    # This is in __new__ because it runs before __init__.
    def __new__(cls, *args, **kwargs):
        if not mainloop._initialized:
            raise ValueError("cannot create widgets without initializing "
                             "the main loop")
        return super(Widget, cls).__new__(cls)

    def __init__(self):
        if not hasattr(self, '_wrapper'):
            # A subclass didn't override this and define a _wrapper.
            cls = type(self)
            raise TypeError("cannot create instances of %s.%s directly, "
                            "instantiate a subclass instead"
                            % (cls.__module__, cls.__name__))

    def __repr__(self):
        parts = self._repr_parts()
        if not parts:
            return super().__repr__()
        cls = type(self)
        return '<%s.%s object, %s>' % (
            cls.__module__, cls.__name__, ', '.join(parts))

    def _repr_parts(self):
        """Return an empty list to make super() usage easier.

        The __repr__ value is constructed from the module and name of
        the class, and the return value of _repr_parts. This method
        should return a list of things that will be joined with a comma
        to create the __repr__. The default __repr__ is used if
        _repr_parts returns an empty list.

        It's recommended to do something like this in _repr_parts:

            def _repr_parts(self):
                return ['thing=stuff'] + super()._repr_parts()
        """
        return []

    @property
    def real_widget(self):
        return self._wrapper.real_widget

    def focus(self):
        """Give the keyboard focus to this widget.

        Focusing a window also brings it in front of other windows.
        It's recommended to first create the widgets and then focus
        one of them to make sure that the widget gets focused correctly
        with all GUI toolkits.
        """
        cls = type(self)
        assert cls.can_focus, "cannot focus %r widgets" % cls.__name__
        self._wrapper.focus()


class Parent(Widget):
    """A base class for widgets that contain other widgets."""

    def iter_children(self, *, recursive=False):
        """Yield all children of this Parent widget.

        If recursive is True, also yield all of the childrens'
        children. This is consistent and works the same way with
        different kinds of Parent widgets.
        """
        # Subclasses should provide _get_children().
        for child in self._get_children():
            yield child
            if recursive and isinstance(child, Parent):
                # yield from is new in Python 3.3.
                for subchild in child.iter_children(recursive=True):
                    yield subchild


@types.add_property('tooltip', type=str, allow_none=True)
@types.add_property('grayed_out', type=bool)
@types.add_property('expand', type=bool, how_many=2)
class Child(Widget):
    """A base class for widgets that can be added to Parent widgets.

    Children don't take a parent argument on initialization, but
    BananaGUI keeps track of the parent internally. When a child is
    added to a parent widget, BananaGUI remembers it. The child can be
    removed from the parent widget and added into it again, but it
    cannot be added to other parent widgets. Example:

        box1 = widgets.Box.horizontal()
        box2 = widgets.Box.horizontal()
        label = widgets.Label()     # label doesn't have a parent
        box1.append(label)          # label's parent is box1
        box1.remove(label)          # label's parent is still box1
        box2.append(label)          # this raises an exception!

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
      tooltip       The widget's tooltip text, or None for no tooltip.
                    None by default.
      grayed_out    True if the widget looks like it's disabled.
                    This can be used to tell the user that the widget
                    can't be used for some reason.
      expand        Two-tuple of horizontal and vertical expanding.
    """

    # TODO: cycle handling
    #   box1 = widgets.Box()
    #   box2 = widgets.Box()
    #   box1.append(box2)
    #   box2.append(box1)   # raise an error with a descriptive message here

    def __init__(self, *, tooltip=None, grayed_out=False,
                 expand=(True, True)):
        self._parent = None     # Other files rely on this also.
        self._tooltip = None
        self._grayed_out = False
        self._expand = (True, True)
        super().__init__()
        self.tooltip = tooltip
        self.grayed_out = grayed_out
        self.expand = expand

    def _repr_parts(self):
        parts = super()._repr_parts()
        if self.tooltip is not None:
            parts.append('tooltip=%r' % self.tooltip)
        if self.grayed_out:
            parts.append('grayed_out=True')
        return parts
