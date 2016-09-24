from bananagui import types


class ButtonBase:
    """Base for other buttons.

    Signals:
        on_click
            Emitted when the button is clicked.

    """

    _bananagui_bases = ('ChildBase',)
    on_click = types.Signal('on_click')


class Button:
    """A button that displays text in it.

    Properties:
        text            RW
            The text of the button.
    """

    _bananagui_bases = ('ButtonBase',)
    text = types.Property('text', required_type=str, default='')
