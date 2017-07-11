from bananagui import _modules
from bananagui._types import Callback
from .base import UpdatingProperty, ChildWidget


class Button(ChildWidget):
    r"""A button that displays text in it.

    .. code-block:: none

         _______________
        |,--------------\
        ||   Click me!  |
        `---------------'
    """

    #can_focus = True

    text = UpdatingProperty.with_attr('_text', doc="""
    The text in the button.

    This is an empty string by default.
    """)

    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        self.text = text

        #: A callback that runs when the button is clicked.
        self.on_click = Callback()

    def __repr__(self):
        return '<%s widget, text=%r>' % (self._module_and_type(), self.text)

    def render(self, parent):
        super().render(parent)
        if _modules.name == 'tkinter':
            self.real_widget = _modules.tk.Button(
                parent.real_widget, command=self.on_click.run)
        elif _modules.name.startswith('gtk'):
            self.real_widget = _modules.Gtk.Button()
            self.real_widget.connect(
                'clicked', (lambda real_widget: self.on_click.run()))
        else:
            raise NotImplementedError

    def render_update(self):
        super().render_update()
        if _modules.name == 'tkinter':
            self.real_widget['text'] = self.text
        elif _modules.name.startswith('gtk'):
            self.real_widget.set_label(self.text)
        else:
            raise NotImplementedError

    def unrender(self):
        if _modules.name == 'tkinter' or _modules.name.startswith('gtk'):
            self.real_widget.destroy()
        else:
            raise NotImplementedError


#@types.add_callback(
#    'on_click', doc="A callback that runs when the button is clicked.")
#@types.add_property(
#    'image', type=images.Image, allow_none=True,
#    doc="""The image displayed in the button.
#
#    This can be None or a :class:`bananagui.images.Image`.
#    """)
#class ImageButton(Child):
#    r"""A button that displays an image.
#
#    .. code-block:: none
#
#        _______________
#       |.--------------\
#       ||       __     |
#       ||   _  / /     |
#       ||    )/ /      |
#       ||   /  /_      |
#       ||  |  |  \     |
#       ||  |_/         |
#       `---------------'
#    """

#    can_focus = True

#    def __init__(self, image=None, **kwargs):
#        self._prop_image = None
#        wrapperclass = _get_wrapper('widgets.buttons:ImageButton')
#        self._wrapper = wrapperclass(self)
#        super().__init__(**kwargs)
#        self.image = image
#
#    def _repr_parts(self):
#        return ['image=' + repr(self.image)] + super()._repr_parts()
