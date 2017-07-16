import abc

from bananagui import _modules, _mainloop
from bananagui._types import UpdatingObject, UpdatingProperty, get_class_name


class Widget(UpdatingObject, metaclass=abc.ABCMeta):
    """A base class for all widgets.

    All widgets inherit from this class, so all widgets have the methods
    that this class has.

    This class inherits from :class:`bananagui.UpdatingObject`.
    """

    # this is in __new__ because it runs before __init__
    def __new__(cls, *args, **kwargs):
        # this is actually needed only for rendering, but requiring it
        # here makes things easier to debug
        _mainloop._check_initialized()

        # this explicit 2-argument super thing is needed i think before
        # 3.7 or something like that, and it doesn't accept *args and
        # **kwargs for some reason 0_o
        return super(Widget, cls).__new__(cls)

    def __init__(self):
        if not hasattr(self, 'real_widget'):
            raise RuntimeError(
                "subclass __init__ didn't set self.real_widget before "
                "calling super().__init__()")

        # TODO: document this behavior
        self.update_state()

    def __repr__(self):
        # hide the fact that it's from bananagui._widgets.something
        # also 'widget' instead of 'object'
        # subclasses do fancier stuff than this
        return '<%s widget>' % get_class_name(type(self))

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

    def update_state(self):
        """Runs :meth:`render_update` if :attr:`real_widget` is not None.

        This implements :meth:`.UpdatingObject.update_state`.
        """
        if self.real_widget is not None:
            self.render_update()


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
