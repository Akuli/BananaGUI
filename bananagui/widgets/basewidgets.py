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

from bananagui import mainloop, types


class Widget:
    """A baseclass for all widgets."""

    can_focus = False

    # This is in __new__ because it runs before __init__.
    def __new__(cls, *args, **kwargs):
        if not mainloop._initialized:
            raise ValueError("cannot create widgets without initializing "
                             "the main loop")
        return super(Widget, cls).__new__(cls)

    def __init__(self):
        """Initialize the widget."""
        if not hasattr(self, '_wrapper'):
            # A subclass didn't override this and define a _wrapper.
            cls = type(self)
            raise TypeError("cannot create instances of %s.%s directly, "
                            "instantiate a subclass instead"
                            % (cls.__module__, cls.__name__))

    def __repr__(self):
        cls = type(self)
        result = '%s.%s object' % (cls.__module__, cls.__name__)
        for part in self._repr_parts():
            result += ', '
            result += part
        return '<' + result + '>'

    def _repr_parts(self):
        """Return an empty list to make super() usage easier.

        The __repr__ value is constructed from the module and name of
        the class, and the return value of _repr_parts. This method
        should return a list of things that will be joined with a comma
        to create the __repr__.

        It's recommended to do something like this in _repr_parts:

            def _repr_parts(self):
                return ['thing=stuff'] + super()._repr_parts()
        """
        return []

    @property
    def real_widget(self):
        """This is the real GUI toolkit's widget that BananaGUI uses."""
        return self._wrapper.widget

    def focus(self):
        """Give the keyboard focus to this widget.

        Widget classes have a ``can_focus`` attribute, and this method
        cannot be called if it's False.

        Focusing a :class:`.Window` or :class:`.Dialog` brings it in
        front of all other windows. When focusing something else it's
        recommended to first create the widgets and then focus one of
        them to make sure that the widget gets focused correctly with
        all GUI toolkits.
        """
        cls = type(self)
        if not cls.can_focus:
            raise TypeError("cannot focus %s.%s widgets"
                            % (cls.__module__, cls.__name__))
        self._wrapper.focus()


@types.add_property(
    'tooltip', type=str, allow_none=True,
    doc="""The widget's tooltip text or None for no tooltip.

    None by default.
    """)
@types.add_property(
    'grayed_out', type=bool,
    doc="""True if the widget looks like it's disabled.

    This can be used to tell the user that the widget can't be used for
    some reason.
    """)
@types.add_property(
    'expand', type=bool, how_many=2,
    doc="""Two-tuple of horizontal and vertical expanding.

    This is ``(True, True)`` by default, so the widget expands in both
    directions.

    When multiple widgets are next to each
    other in a container, at least one of them should expand in the
    container's direction. Like this:

    .. code-block:: none
    
       ,------------------------------------------------.
       |   non-   |                                     |
       |expanding |           expanding widget          |
       |  widget  |                                     |
       `------------------------------------------------'
    
    Not like this:
    
    .. code-block:: none
    
       ,------------------------------------------------.
       |   non-   |   non-   |                          |
       |expanding |expanding |       empty space        |
       |  widget  |  widget  |                          |
       `------------------------------------------------'
    
    This way the children will behave consistently with all GUI
    toolkits. You can use a Dummy widget to fill the empty space if
    needed:
 
    .. code-block:: none
    
       ,------------------------------------------------.
       |   non-   |   non-   |                          |
       |expanding |expanding |       Dummy widget       |
       |  widget  |  widget  |                          |
       `------------------------------------------------'
    """)
class Child(Widget):
    """Base class for widgets that can be added to :class:`.Parent` widgets.

    BananaGUI keeps track of the parent internally. When a child is
    added to a parent widget, BananaGUI remembers it. The child can be
    removed from the parent widget and added into it again, but it
    cannot be added to other parent widgets. For example:

    .. code-block:: python

       box1 = widgets.Box()
       box2 = widgets.Box()
       label = widgets.Label()     # label doesn't have a parent
       box1.append(label)          # label's parent is now box1
       box1.remove(label)          # label's parent is still box1
       box2.append(label)          # this raises an exception!
    """

    # TODO: cycle handling
    #   box1 = widgets.Box()
    #   box2 = widgets.Box()
    #   box1.append(box2)
    #   box2.append(box1)   # raise an error with a descriptive message here

    def __init__(self, *, tooltip=None, grayed_out=False,
                 expand=(True, True)):
        """Set arguments as attributes."""
        self._parent = None     # Other files rely on this also.
        self._prop_tooltip = None
        self._prop_grayed_out = False
        self._prop_expand = (True, True)
        super().__init__()
        self.tooltip = tooltip
        self.grayed_out = grayed_out
        self.expand = expand
