"""This module contains simple functions for clipboard things."""

from bananagui import _get_wrapper, mainloop

__all__ = ['set_text', 'get_text']


def _initcheck():
    if not mainloop._initialized:
        raise RuntimeError("initialize the main loop before using "
                           "the clipboard")


def set_text(text: str):
    """Set text to the clipboard."""
    _initcheck()
    _get_wrapper('clipboard:set_text')(text)


def get_text():
    """Return the text that is currently on the clipboard.

    This returns None if there is no text on the clipboard.
    """
    _initcheck()
    return _get_wrapper('clipboard:get_text')()
