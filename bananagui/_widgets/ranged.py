from bananagui import _get_wrapper, Orient, types
from .basewidgets import Child


def _valuecheck(widget, value):
    if value not in widget.valuerange:
        raise ValueError("value %r is out of %r"
                         % (value, widget.valuerange))


@types.add_property(
    'value', extra_setter=_valuecheck, add_changed=True,
    doc="""The widget's current value.

    This needs to be in :attr:`~valuerange` and it's the smallest value
    of valuerange by default.
    """)
class _Ranged:
    """Implement valuerange and value BananaGUI properties."""
    # Subclasses should get a valuerange argument on initialization,
    # set the _valuerange attribute to it and set the _value attribute
    # to min() of that range.

    def __init__(self, *args, **kwargs):
        if len(self.valuerange) < 2:
            raise ValueError("valuerange %r contains too little values"
                             % (self.valuerange,))
        if self.valuerange.step < 0:
            raise ValueError("valuerange has negative step")
        super().__init__(*args, **kwargs)

    @property
    def valuerange(self):
        """The range of allowed values set on initialization."""
        return self._prop_valuerange

    def _repr_parts(self):
        return [
            'value=' + repr(self.value),
            'valuerange=' + repr(self.valuerange),
        ] + super()._repr_parts()


class Spinbox(_Ranged, Child):
    """A widget for selecting an integer.

    .. code-block:: none

       ,-----------------------.
       | 123           | + | - |
       `-----------------------'

    You can use Entry widgets for selecting numbers, but this widget
    provides nicer + and - buttons.

    Spinboxes can't be used with floats because the allowed values are
    represented by a Python range object, so you need to use an Entry if
    you want to use floats.
    """

    can_focus = True

    def __init__(self, valuerange: range, *, value=None, **kwargs):
        """Initialize the spinbox."""
        self._prop_valuerange = valuerange
        self._prop_value = min(valuerange)
        wrapperclass = _get_wrapper('widgets.ranged:Spinbox')
        self._wrapper = wrapperclass(self, valuerange)
        super().__init__(**kwargs)
        if value is not None:
            self.value = value


class Slider(_Ranged, Child):
    """A slider for selecting a number.

    .. code-block:: none

       |
       O   -----O--------
       |
       |
       |

    Currently floats aren't supported. If you want float support, let
    me know and I'll implement it.
    """

    def __init__(self, valuerange: range, orient=Orient.HORIZONTAL, *,
                 value=None, **kwargs):
        """Initialize the slider."""
        self.__orient = Orient(orient)
        self._prop_valuerange = valuerange
        self._prop_value = min(valuerange)
        wrapperclass = _get_wrapper('widgets.ranged:Slider')
        self._wrapper = wrapperclass(self, self.__orient, valuerange)
        super().__init__(**kwargs)
        if value is not None:
            self.value = value

    @property
    def orient(self):
        """The orientation of the slider.

        This is always a :class:`bananagui.Orient` member.
        """
        return self.__orient

    def _repr_parts(self):
        parts = super()._repr_parts()
        if self.orient == Orient.VERTICAL:
            # Not the default
            parts.insert(0, 'vertical')
        return parts
