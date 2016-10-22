import bananagui
from bananagui import _base, utils
from .basewidgets import Child


@utils.baseclass
@bananagui.document_props
class BaseButton(_base.BaseButton, Child):
    """Base for other buttons."""

    on_click = bananagui.BananaSignal(
        'on_click', doc="This is emitted when the button is clicked.")


@bananagui.document_props
class Button(_base.Button, BaseButton):
    """A button that displays text in it."""

    text = bananagui.BananaProperty(
        'text', type=str, default='',
        doc="The text in the button.")


@bananagui.document_props
class ImageButton(_base.ImageButton, BaseButton):
    """A button that displays an image."""
    imagepath = bananagui.BananaProperty.imagepath(
        'imagepath',
        doc="Path to the image that is displayed in the button.")
