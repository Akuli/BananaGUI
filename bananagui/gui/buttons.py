from bananagui import _base, Property, Signal, bananadoc
from bananagui.utils import baseclass
from .bases import Child


@baseclass
@bananadoc
class BaseButton(_base.BaseButton, Child):
    """Base for other buttons."""

    on_click = Signal(
        'on_click', doc="This is emitted when the button is clicked.")


@bananadoc
class Button(_base.Button, BaseButton):
    """A button that displays text in it."""

    text = Property('text', type=str, default='',
                    doc="The text in the button.")


@bananadoc
class ImageButton(_base.ImageButton, BaseButton):
    """A button that displays an image."""
    imagepath = Property.imagepath(
        'imagepath',
        doc="Path to the image that is displayed in the button.")
