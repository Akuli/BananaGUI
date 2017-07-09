from bananagui import _get_wrapper, images, types
from .basewidgets import Child


@types.add_callback(
    'on_click', doc="""A callback that runs when the button is clicked.""")
@types.add_property(
    'text', type=str, doc="""The text in the button.

    An empty string by default.
    """)
class Button(Child):
    r"""A button that displays text in it.

    .. code-block:: none

        _______________
       |,--------------\
       ||   Click me!  |
       `---------------'
    """

    can_focus = True

    def __init__(self, text='', **kwargs):
        self._prop_text = ''
        wrapperclass = _get_wrapper('widgets.buttons:Button')
        self._wrapper = wrapperclass(self)
        super().__init__(**kwargs)
        self.text = text

    def _repr_parts(self):
        return ['text=' + repr(self.text)] + super()._repr_parts()


@types.add_callback(
    'on_click', doc="A callback that runs when the button is clicked.")
@types.add_property(
    'image', type=images.Image, allow_none=True,
    doc="""The image displayed in the button.

    This can be None or a :class:`bananagui.images.Image`.
    """)
class ImageButton(Child):
    r"""A button that displays an image.

    .. code-block:: none

        _______________
       |.--------------\
       ||       __     |
       ||   _  / /     |
       ||    )/ /      |
       ||   /  /_      |
       ||  |  |  \     |
       ||  |_/         |
       `---------------'
    """

    can_focus = True

    def __init__(self, image=None, **kwargs):
        self._prop_image = None
        wrapperclass = _get_wrapper('widgets.buttons:ImageButton')
        self._wrapper = wrapperclass(self)
        super().__init__(**kwargs)
        self.image = image

    def _repr_parts(self):
        return ['image=' + repr(self.image)] + super()._repr_parts()
