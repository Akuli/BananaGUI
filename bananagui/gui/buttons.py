import bananagui
from bananagui import _base, utils
from . import bases


@utils.baseclass
@bananagui.bananadoc
class BaseButton(_base.BaseButton, bases.Child):
    """Base for other buttons."""

    on_click = bananagui.Signal(
        'on_click', doc="This is emitted when the button is clicked.")


@bananagui.bananadoc
class Button(_base.Button, BaseButton):
    """A button that displays text in it."""

    text = bananagui.Property('text', type=str, default='',
                              doc="The text in the button.")


@bananagui.bananadoc
class ImageButton(_base.ImageButton, BaseButton):
    """A button that displays an image."""
    imagepath = bananagui.Property.imagepath(
        'imagepath',
        doc="Path to the image that is displayed in the button.")
