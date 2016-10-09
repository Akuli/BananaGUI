from bananagui import _base
from bananagui.types import Property, Signal, bananadoc
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
    # TODO: The imagepath property is just like in labels.py.
    imagepath = Property.imagepath(
        'imagepath',
        doc="Path to the image that will be displayed in the button.")

    def _bananagui_set_imagepath(self, path):
        assert path is None or os.path.isfile(path), \
            "%r is not a path to a file" % (path,)
        super()._bananagui_set_imagepath(path)
