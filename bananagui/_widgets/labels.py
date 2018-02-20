from bananagui import _modules
from .base import Align, UpdatingProperty, ChildWidget


class Label(ChildWidget):
    """A widget that displays text.

    .. code-block:: none

       ,---------------.
       |  Hello World! |
       `---------------'

    The align will be converted to a :class:`bananagui.Align` member.
    ``**kwargs`` are passed to :class:`bananagui.Widget`.

    .. seealso:: `Text editing widgets`_.
    """
    # TODO: Add fonts and colors?

    def __init__(self, text='', *, align=Align.CENTER, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.align = align

    def __repr__(self):
        return '<%s widget, text=%r>' % (self._get_class_name(), self.text)

    @UpdatingProperty.updater_with_attr('_text')
    def text(self):
        """The text in the label."""
        if _modules.name == 'tkinter':
            self.real_widget['text'] = self.text
        elif _modules.name.startswith('gtk'):
            self.real_widget.set_text(self.text)
        else:   # pragma: no cover
            raise NotImplementedError

    # TODO: implement this
    @UpdatingProperty.updater_with_attr('_align')
    def align(self):
        r"""How the text is aligned in the label.

        If the text contains ``\n`` characters, this also determines how the
        text is justified.

        This needs to be a :class:`bananagui.Align` member.
        """
        pass

    def render(self, parent):
        super().render(parent)
        if _modules.name == 'tkinter':
            self.real_widget = _modules.tk.Label(parent.real_widget)
        elif _modules.name.startswith('gtk'):
            self.real_widget = _modules.Gtk.Label()
        else:   # pragma: no cover
            raise NotImplementedError


#@types.add_property(
#    'image', type=images.Image, allow_none=True,
#    doc="""The image displayed in the button.
#
#    This should be None or a :class:`bananagui.images.Image`.
#    """)
#class ImageLabel(Child):
#    r"""A widget that displays an image.
#
#       ,---------------.
#       |        __     |
#       |    _  / /     |
#       |     )/ /      |
#       |    /  /_      |
#       |   |  |  \     |
#       |   |_/         |
#       `---------------'
#    """
#
#    def __init__(self, image=None, **kwargs):
#        """Initialize the image label."""
#        self._prop_image = None
#        wrapperclass = _get_wrapper('widgets.labels:ImageLabel')
#        self._wrapper = wrapperclass(self)
#        super().__init__(**kwargs)
#        self.image = image
#
#    def _repr_parts(self):
#        return ['image=' + repr(self.image)] + super()._repr_parts()
