from bananagui import _base
from bananagui.types import Property


def set_clipboard_text(text: str):
    """Set text to the clipboard."""
    _base.set_clipboard_text(text)


def get_clipboard_text():
    """Return the text that is currently on the clipboard."""
    return _base.get_clipboard_text()
