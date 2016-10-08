from gi.repository import Gtk, Gdk


clipboard = None

def init_clipboard():
    global clipboard
    if clipboard is None:
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)


def set_clipboard_text(text):
    init_clipboard()
    clipboard.set_text(text, -1)
    clipboard.store()


def get_clipboard_text():
    init_clipboard()
    # clipboard.wait_for_text() doesn't block if there's no text on the
    # clipboard, it returns None.
    result = clipboard.wait_for_text()
    if result is None:
        return ''
    return result
