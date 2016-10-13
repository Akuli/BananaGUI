from bananagui import _base


def set_clipboard_text(text: str) -> None:
    """Set text to the clipboard."""
    _base.set_clipboard_text(text)


def get_clipboard_text() -> str:
    """Return the text that is currently on the clipboard."""
    return _base.get_clipboard_text()
