from bananagui import _get_wrapper, Orient, types
from .basewidgets import Child

# TODO: A RadioButton, or _RadioButton and RadioButtonManager.
# TODO: move Checkbox, Radiostuff and stuff like that to a checkboxes.py?


@types.add_property('text', type=str, doc="The text next to the checkmark.")
@types.add_property('checked', type=bool, add_changed=True,
                    doc="True if the checkbox is currently checked.")
class Checkbox(Child):
    """A widget that can be checked.

    .. code-block:: none

       ,-------------------.
       |   |   Check me!   |
       `-------------------'

       ,-------------------.
       | X |  Uncheck me!  |
       `-------------------'

    The Checkbox widget has nothing to do with the :class:`.Box` widget.
    """

    can_focus = True

    def __init__(self, text='', *, checked=False, **kwargs):
        """Initialize the checkbox and set arguments as attributes."""
        self._prop_text = ''
        self._prop_checked = False
        wrapperclass = _get_wrapper('widgets.misc:Checkbox')
        self._wrapper = wrapperclass(self)
        super().__init__(**kwargs)
        self.text = text
        self.checked = checked

    def _repr_parts(self):
        return ['text=%r' % self.text,
                'checked=%r' % self.checked] + super()._repr_parts()


class Dummy(Child):
    """An empty widget.

    .. code-block:: none

       ,-----------.
       |           |
       |           |
       `-----------'

    This is useful for creating layouts with empty space that must be
    filled with something. See :attr:`.Child.expand` for more info.
    """

    def __init__(self, **kwargs):
        """Set up the dummy."""
        wrapperclass = _get_wrapper('widgets.misc:Dummy')
        self._wrapper = wrapperclass(self)
        super().__init__(**kwargs)


class Separator(Child):
    """A horizontal or vertical line.

    .. code-block:: none

                       ||
           Widget 1    ||
       ================||  Widget 3
           Widget 2    ||
                       ||

    Usually there's no need to add separators between widgets, but they
    are sometimes useful.
    """

    def __init__(self, orient=Orient.HORIZONTAL, **kwargs):
        """Initialize the separator.

        The orient will be converted to a bananagui.Orient member.
        """
        self.__orient = Orient(orient)
        # Make the separator expand correctly by default.
        if self.__orient == Orient.HORIZONTAL:
            kwargs.setdefault('expand', (True, False))
        if self.__orient == Orient.VERTICAL:
            kwargs.setdefault('expand', (False, True))
        wrapperclass = _get_wrapper('widgets.misc:Separator')
        self._wrapper = wrapperclass(self, self.__orient)
        super().__init__(**kwargs)

    def _repr_parts(self):
        parts = super()._repr_parts()
        if self.orient == Orient.VERTICAL:
            # Not the default.
            parts.insert(0, 'vertical')
        return parts

    @property
    def orient(self):
        """The orient set on initialization.

        This is always a :class:`bananagui.Orient` member.
        """
        return self.__orient
