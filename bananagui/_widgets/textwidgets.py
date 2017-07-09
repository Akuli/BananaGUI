from bananagui import _get_wrapper, types
from .basewidgets import Child


# TODO: separate grayed_out and editable
@types.add_property('text', type=str, add_changed=True,
                    doc="The text in the widget.")
class TextBase(Child):
    """A base class for text editing widgets.

    Setting *grayed_out* to True means that the user can't edit the
    text.
    """
    # TODO: Add fonts and colors.

    can_focus = True

    def __init__(self, text='', **kwargs):
        self._prop_text = ''
        super().__init__(**kwargs)
        self.text = text

    def select_all(self):
        """Select all text in the widget."""
        self._wrapper.select_all()


@types.add_property(
    'secret', type=bool,
    doc="""True if the text is hidden with stars or balls.

    It's also impossible to copy-paste from a secret entry. This is
    useful for asking a password.
    """)
class Entry(TextBase):
    """A one-line text widget.

    .. code-block:: none

       ,-----------------------.
       | Enter something...    |
       `-----------------------'

    .. seealso:: `Number selecting widgets`_.
    """

    def __init__(self, text='', *, secret=False, **kwargs):
        """Initialize the entry."""
        self._prop_secret = False
        wrapperclass = _get_wrapper('widgets.textwidgets:Entry')
        self._wrapper = wrapperclass(self)
        super().__init__(text=text, **kwargs)
        self.secret = secret

    def _repr_parts(self):
        parts = ['text=%r' % self.text] + super()._repr_parts()
        if self.secret:
            parts.append('secret=True')
        return parts


# TODO: text wrapping.
# TODO: text alignment?
# TODO: make this behave like a list of lines.
@types.add_property(
    'tab', type=str, doc="The character that pressing tab inserts.")
class TextEdit(TextBase):
    """A multiline text widget.

    .. code-block:: none

       ,-----------.
       | Line 0    |
       | Line 1    |
       | Line 2    |
       | Line 3    |
       |           |
       `-----------'

    .. note:: The TextEdit widget doesn't work that well right now. I'll
              make a better TextEdit widget when I have time and it will
              have a different API, so don't rely on this widget.
    """

    def __init__(self, text='', *, tab='\t', **kwargs):
        """Initialize the TextEdit."""
        self._prop_tab = '\t'
        wrapperclass = _get_wrapper('widgets.textwidgets:TextEdit')
        self._wrapper = wrapperclass(self)
        super().__init__(text=text, **kwargs)
        self.tab = tab

    # We can't add the whole text here because it would be too long.
    def _repr_parts(self):
        linecount = self.text.count('\n') + 1
        amount = "one line" if linecount == 1 else "%d lines" % linecount
        return super()._repr_parts() + ["contains %s of text" % amount]
