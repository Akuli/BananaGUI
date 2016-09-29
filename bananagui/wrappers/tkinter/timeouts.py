import tkinter as tk


class Timeout:

    @classmethod
    def add_timeout(cls, milliseconds, callback):
        try:
            # At the time of writing this, tkinter stores its root
            # widget in a _default_root variable.
            widget = tk._default_root
        except AttributeError:
            # We need a dummy widget.
            widget = tk.Label()

        def real_callback():
            result = callback()
            if result == cls.RUN_AGAIN:
                widget.after(milliseconds, real_callback)
            assert result is not None, \
                "callbacks need to return None or Timeout.RUN_AGAIN"

        widget.after(milliseconds, real_callback)
