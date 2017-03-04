from bananagui import _get_wrapper, Align, images, types
from .basewidgets import Child


@types.add_property('text', type=str, doc="The text in the label.")
@types.add_property(
    'align', type=Align,
    doc="""How the text is aligned.

    This needs to be a :class:`bananagui.Align` member.
    """)
class Label(Child):
    """A widget that displays text.

    .. code-block:: none

       ,---------------.
       |  Hello World! |
       `---------------'

    .. seealso:: `Text editing widgets`_.
    """
    # TODO: Add fonts and colors?

    def __init__(self, text='', *, align=Align.CENTER, **kwargs):
        """Initialize the label.

        The align will be converted to a :class:`bananagui.Align` member.
        """
        self._prop_text = ''
        self._prop_align = Align.CENTER
        wrapperclass = _get_wrapper('widgets.labels:Label')
        self._wrapper = wrapperclass(self)
        super().__init__(**kwargs)
        self.text = text
        self.align = Align(align)

    def _repr_parts(self):
        return ['text=' + repr(self.text)] + super()._repr_parts()


@types.add_property(
    'image', type=images.Image, allow_none=True,
    doc="""The image displayed in the button.

    This should be None or a :class:`bananagui.images.Image`.
    """)
class ImageLabel(Child):
    r"""A widget that displays an image.

    .. code-block:: none

       ,---------------.
       |        __     |
       |    _  / /     |
       |     )/ /      |
       |    /  /_      |
       |   |  |  \     |
       |   |_/         |
       `---------------'
    """

    def __init__(self, image=None, **kwargs):
        """Initialize the image label."""
        self._prop_image = None
        wrapperclass = _get_wrapper('widgets.labels:ImageLabel')
        self._wrapper = wrapperclass(self)
        super().__init__(**kwargs)
        self.image = image

    def _repr_parts(self):
        return ['image=' + repr(self.image)] + super()._repr_parts()
