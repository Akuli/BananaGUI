from bananagui.core import Property, bases


class LabelBase(bases.ChildBase):
    """A label base widget."""


class TextLabel(LabelBase):

    """A label with text in it.

    Properties:
        text            RW
            The label's text. An empty string by default.
    """

    text = Property(converter=str, default='')
