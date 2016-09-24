import tkinter as tk

import bananagui

# TODO: fix this


def add_timeout(seconds, callback):
    try:
        # At the time of writing this, tkinter stores its root widget in
        # a _default_root variable.
        widget = tk._default_root
    except AttributeError:
        # Let's assume that the user has called init() and we're not
        # going to end up with an automatically created root window.
        widget = tk.Label()

    if widget is None:
        # The _default_root variable is None when a root window hasn't
        # been created.
        raise RuntimeError("initialize BananaGUI before creating callbacks")

    milliseconds = int(seconds * 1000)

    def real_callback():
        result = callback()
        if result == bananagui.RUN_AGAIN:
            widget.after(milliseconds, real_callback)
        elif result != bananagui.STOP:
            raise ValueError("expected bananagui.RUN_AGAIN or bananagui.STOP, "
                             "got %r" % (result,))

    widget.after(milliseconds, real_callback)
