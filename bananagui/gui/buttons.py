from bananagui import _base
from bananagui.types import Property, Signal, bananadoc
from .bases import ChildBase


@bananadoc
class ButtonBase(_base.ButtonBase, ChildBase):
    """Base for other buttons."""

    on_click = Signal(
        'on_click', doc="This is emitted when the button is clicked.")


@bananadoc
class Button(_base.Button, ButtonBase):
    """A button that displays text in it.

    Properties:
        text            RW
            The text of the button.
    """

    text = Property('text', required_type=str, default='',
                    doc="The text in the button.")


# TODO: A button type suitable for toolbars. A toolbar class somewhere.
