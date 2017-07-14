import abc

from bananagui import _modules, mainloop


class UpdatingProperty(property):
    """A property that calls :meth:`Widget.render_update` automatically.

    UpdatingProperty works otherwise just like a regular :class:`property`,
    but after setting the value it also calls the widget's
    :meth:`render_update <Widget.render_update>`` method. If the
    widget's ``real_widget`` attribute is None the widget hasn't been
    rendered yet, and this behaves just like a regular property.
    """

    def _make_setter(self, user_setter):
        # no need to use functools.wraps because setter docstrings
        # aren't used anywhere anyway
        def real_setter(widget, value):
            user_setter(widget, value)
            if widget.real_widget is not None:
                widget.render_update()

        return real_setter

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        if fset is not None:
            fset = self._make_setter(fset)
        super().__init__(fget, fset, fdel, doc)

    def setter(self, func):
        return super().setter(self._make_setter(func))

    @classmethod
    def with_attr(cls, attrname, *, doc=None):
        """A convenient way to create a minimal property.

        This...

        .. code-block:: python

            class Thing(bananagui.Widget):
                stuff = UpdatingProperty.with_attr('_stuff')

        ...is roughly equivalent to this::

            class Thing(bananagui.Widget):

                @UpdatingProperty
                def stuff(self):
                    return self._stuff

                @stuff.setter
                def stuff(self, value):
                    self._stuff = value
        """
        def getter(self):
            return getattr(self, attrname)

        def setter(self, value):
            setattr(self, attrname, value)

        return cls(getter, setter, doc=doc)


class Widget(metaclass=abc.ABCMeta):
    """A base class for all widgets.

    All widgets inherit from this class, so all widgets have the methods
    that this class has.
    """

    # this is in __new__ because it runs before __init__
    def __new__(cls, *args, **kwargs):
        # this is actually needed only for rendering, but requiring it
        # here makes things easier to debug
        mainloop._check_initialized()

        # this explicit 2-argument super thing is needed i think before
        # 3.7 or something like that, and it doesn't accept *args and
        # **kwargs for some reason 0_o
        return super(Widget, cls).__new__(cls)

    def __init__(self):
        if not hasattr(self, 'real_widget'):
            raise RuntimeError(
                "subclass __init__ didn't create a real_widget before "
                "calling super().__init__()")
        if self.real_widget is not None:
            self.render_update()

    # this is also used in subclasses
    @classmethod
    def _module_and_type(cls):
        modulename = cls.__module__
        if modulename.startswith('bananagui.'):
            modulename = 'bananagui'
        return modulename + '.' + cls.__name__

    def __repr__(self):
        # hide the fact that it's from bananagui._widgets.something
        # also 'widget' instead of 'object'
        return '<%s widget at %#x>' % (self._module_and_type(), id(self))

    @abc.abstractmethod
    def render_update(self):
        """Do any changes to the widget necessary.

        This is ran when some property that effects how the widget
        should look is changed. For example, ``label.text = 'hi'`` first
        sets ``'hi'`` to a non-public ``label._text`` attribute, and
        then runs ``label.render_update()``. :class:`UpdatingProperty`
        is an easy way to create properties like this.

        Implementations of this should call ``super().render_update()``.
        """


class ChildWidget(Widget, metaclass=abc.ABCMeta):
    """A widget that goes inside another widget.

    Child widgets aren't displayed to the user right away when they are
    created. Actually the real GUI toolkit's widget isn't created at all
    until the :meth:`~render` method is called.
    """

    tooltip = UpdatingProperty.with_attr('_tooltip', doc="""
    The widget's tooltip text as a string or None for no tooltip.

    This is None by default.
    """)

    grayed_out = UpdatingProperty.with_attr('_grayed_out', doc="""
    True if the widget looks like it's disabled.

    This can be used to tell the user that the widget can't be used for
    some reason.
    """)

    # TODO: in most toolkits (Gtk2 and tkinter) expandiness is managed
    # by the parent widget that this widget is in, so this needs a good
    # way to tell the parent widget that this widget's expandiness has
    # changed, currently this whole expand property does nothing :(
    expand = UpdatingProperty.with_attr('_expand', doc="""
    Two-tuple of horizontal and vertical expanding.

    This is ``(True, True)`` by default, so the widget expands in both
    directions.

    When multiple widgets are next to each other in a parent widget, at
    least one of them should expand in the layout widget's direction.
    Like this:

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
    toolkits. You can use a :class:`.Dummy` widget to fill the empty
    space if needed:

    .. code-block:: none

        ,------------------------------------------------.
        |   non-   |   non-   |                          |
        |expanding |expanding |       Dummy widget       |
        |  widget  |  widget  |                          |
        `------------------------------------------------'
    """)

    def __init__(self, *, tooltip=None, grayed_out=False, expand=(True, True)):
        self.real_widget = None
        super().__init__()
        self.tooltip = tooltip
        self.grayed_out = grayed_out
        self.expand = expand

    @abc.abstractmethod
    def render(self, parent):
        """This should create a widget into *parent*.

        The created widget should also be set to ``self.real_widget``,
        and the parent will always be a :class:`bananagui.Widget`.

        Concrete implementations should call ``super().render(parent)``.
        """
        if self.real_widget is not None:
            raise RuntimeError("the same widget cannot be shown in two "
                               "places at the same time")

    @abc.abstractmethod
    def unrender(self):
        """This should destroy ``self.real_widget`` and set it to None.

        Concrete implementations should call ``super().unrender()``.
        """
        assert self.real_widget is not None, \
            "render() wasn't called or it didn't set self.real_widget"

    def render_update(self):
        if _modules.name == 'tkinter':
            _modules.tk_tooltip.set_tooltip(self.real_widget, self.tooltip)
            try:
                self.real_widget['state'] = (
                    'disabled' if self.grayed_out else 'normal')
            except _modules.tk.TclError:
                # some ttk widgets don't seem to support the state option
                pass

        elif _modules.name.startswith('gtk'):
            # set_tooltip_text() doesn't take None on Gtk 2 for some reason
            if _modules.name == 'gtk2' and self.tooltip is None:
                self.real_widget.set_tooltip_markup(None)
            else:
                self.real_widget.set_tooltip_text(self.tooltip)
            self.real_widget.set_sensitive(not self.grayed_out)

        else:
            raise NotImplementedError
