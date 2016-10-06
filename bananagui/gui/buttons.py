from bananagui import _base
from bananagui.types import Property, Signal, bananadoc
from bananagui.utils import baseclass
from .bases import Child


@baseclass
@bananadoc
class BaseButton(_base.ButtonBase, Child):
    """Base for other buttons."""

    on_click = Signal(
        'on_click', doc="This is emitted when the button is clicked.")


@bananadoc
class Button(_base.Button, BaseButton):
    """A button that displays text in it.

    Properties:
        text            RW
            The text of the button.
    """

    text = Property('text', type=str, default='', settable=True,
                    doc="The text in the button.")


# TODO: A button type suitable for toolbars. A toolbar class somewhere.
