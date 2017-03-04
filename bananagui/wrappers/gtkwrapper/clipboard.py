from gi.repository import Gtk, Gdk


_clipboard = None


def _init_clipboard():
    global _clipboard
    if _clipboard is None:
        _clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)


def set_text(text):
    _init_clipboard()
    _clipboard.set_text(text, -1)
    _clipboard.store()


def get_text():
    _init_clipboard()
    # clipboard.wait_for_text() returns None if there's no text on the
    # clipboard. I have no idea why it's called waiting because it
    # doesn't actually wait.
    return _clipboard.wait_for_text()
