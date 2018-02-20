import abc
import enum

from bananagui import _modules, _mainloop
from bananagui._types import UpdatingObject, UpdatingProperty, Callback


class Orient(enum.IntEnum):
    HORIZONTAL = 1
    VERTICAL = 2


class Align(enum.IntEnum):
    LEFT = 1
    CENTER = 2
    RIGHT = 3

    # These are aliases because LEFT and RIGHT are used more often.
    TOP = LEFT
    BOTTOM = RIGHT


class Widget(UpdatingObject, metaclass=abc.ABCMeta):
    """A base class for all widgets.

    All widgets inherit from this class, so all widgets have the methods
    that this class has.

    This class inherits from :class:`bananagui.UpdatingObject`.
    """

    # this is in __new__ because it runs before __init__
    def __new__(cls, *args, **kwargs):
        # this class has no abstract methods, but it should still not be
        # used directly
        if cls is Widget:
            raise TypeError("cannot create instances of Widget directly, "
                            "instantiate a subclass of Widget instead")
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
                "subclasses of Widget must set self.real_widget before "
                "calling Widget.__init__()")

    def needs_updating(self):
        """Returns True if the widget has been rendered.

        This implements :meth:`.UpdatingObject.update_state`.
        """
        return (self.real_widget is not None)

    def _get_class_name(self):
        # hide the fact that it's from bananagui._widgets.something
        # also 'widget' instead of 'object'
        cls = type(self)
        if cls.__module__.startswith('bananagui.'):
            return 'bananagui.%s' % cls.__name__
        return '%s.%s' % (cls.__module__, cls.__name__)

    def __repr__(self):
        return '<%s widget>' % self._get_class_name()


class ChildWidget(Widget, metaclass=abc.ABCMeta):
    """A widget that goes inside another widget.

    Child widgets aren't displayed to the user right away when they are
    created. Actually the real GUI toolkit's widget isn't created at all
    until the :meth:`~render` method is called.
    """

    def __init__(self, *, tooltip=None, grayed_out=False, expand=(True, True)):
        self.real_widget = None
        super().__init__()
        self.tooltip = tooltip
        self.grayed_out = grayed_out
        self._expand = expand
        self._on_expand_changed = Callback(bool, bool)

    @UpdatingProperty.updater_with_attr('_tooltip')
    def tooltip(self):
        """The widget's tooltip text as a string or None for no tooltip.

        This is None by default.
        """
        if _modules.name == 'tkinter':
            _modules.tk_tooltip.set_tooltip(self.real_widget, self.tooltip)
        elif _modules.name.startswith('gtk'):
            # set_tooltip_text() doesn't take None on Gtk 2 for some reason
            if _modules.name == 'gtk2' and self.tooltip is None:
                self.real_widget.set_tooltip_markup(None)
            else:
                self.real_widget.set_tooltip_text(self.tooltip)
        else:  # pragma: no cover
            raise NotImplementedError

    @UpdatingProperty.updater_with_attr('_grayed_out')
    def grayed_out(self):
        """True if the widget looks like it's disabled.

        This can be used to tell the user that the widget can't be used for
        some reason.
        """
        if _modules.name == 'tkinter':
            try:
                self.real_widget['state'] = (
                    'disabled' if self.grayed_out else 'normal')
            except _modules.tk.TclError as e:
                raise NotImplementedError(
                    "cannot gray out ttk widgets yet :(") from e
        elif _modules.name.startswith('gtk'):
            self.real_widget.set_sensitive(not self.grayed_out)
        else:   # pragma: no cover
            raise NotImplementedError

    # in many toolkits, expandiness is managed by the parent widget
    @UpdatingProperty.updater_with_attr('_expand')
    def expand(self):
        """Two-tuple of horizontal and vertical expanding.

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
        """
        horizontal, vertical = self.expand
        self._on_expand_changed.run(horizontal, vertical)   # FIXME: use this!

    @abc.abstractmethod
    def render(self, parent):
        """This should create a widget into *parent*.

        The created widget should be set to ``self.real_widget``, and
        the parent will always be a :class:`bananagui.Widget`. Use
        ``parent.real_widget`` to access the real parent widget.

        Concrete implementations should call ``super().render(parent)``.
        """
        if self.real_widget is not None:
            raise RuntimeError("the same widget cannot be shown in two "
                               "places at the same time")

    def unrender(self):
        """Destroy ``self.real_widget`` and set it to None."""
        assert self.real_widget is not None, \
            "render() wasn't called or it didn't set self.real_widget"
        if _modules.name == 'tkinter' or _modules.name.startswith('gtk'):
            self.real_widget.destroy()
        else:   # pragma: no cover
            raise NotImplementedError
        self.real_widget = None


class Parent(Widget, metaclass=abc.ABCMeta):
    """A base class for widgets that contain other widgets."""

    @abc.abstractmethod
    def children(self):
        """Return a list of this widget's children.

        Dictionaries have a ``keys()`` method that returns a set-like
        view of the keys. This method is similar, but this returns a
        list of widgets.

        Subclasses of Parent provide different kinds of ways to access
        the children, but they all provide a children method that works
        consistently.
        """

    def _prepare_add(self, child):
        """Make sure child can be added to self and make it ready for it."""
        if child in self.children():
            raise ValueError("cannot add %r twice" % (child,))
        
    def _prepare_remove(self, child):
        """Make sure that a child can be removed from self."""
        if child not in self.children():
            raise ValueError("cannot remove %r, it hasn't been added"
                             % (child,))

    # subclasses use this in __repr__()
    def _content_info(self):
        length = len(self.children())
        if length == 0:
            return 'nothing'
        if length == 1:
            # TODO: use 'an' instead of 'a' when needed
            classname = list(self.children())[0]._get_class_name()
            if classname[0].upper() in 'AEIOUY':
                return 'an ' + classname
            return 'a ' + classname
        return '%d widgets' % length
