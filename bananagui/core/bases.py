"""Various base widgets for other widgets."""

import bananagui
from bananagui.core import ObjectBase, Property


class WidgetBase(ObjectBase):
    """A widget baseclass.

    Properties:
        real_widget     R
            The real GUI toolkit widget that's being wrapped.
        tooltip         RW
            The widget's tooltip text. None by default.
    """

    real_widget = Property()
    tooltip = Property(converter=str, allow_none=True, default=None)


class ParentBase(WidgetBase):
    """A widget that child widgets can use as their parent."""


class ChildBase(WidgetBase):
    """A widget that can be added to a container.

    Children take a parent argument on initialization. The parent
    property can be used to retrieve it, but the parent cannot be
    changed afterwards.

    Properties:
        parent          R
            The parent of this widget.
        grayed_out      RW
            True if the widget is grayed out, False otherwise.
    """

    parent = Property(required_type=ParentBase)
    grayed_out = Property(converter=bool, default=False)

    def __init__(self, parent):
        super().__init__()
        self.parent.raw_set(parent)


class BinBase(ParentBase):
    """A widget that contains one child widget or no children at all.

    Properties:
        child           RW
            The child in the widget, None by default.
            Setting this to None removes the child.
    """

    child = Property(allow_none=True, default=None, required_type=WidgetBase)
