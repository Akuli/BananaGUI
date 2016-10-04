from . import mainloop


def add_timeout(milliseconds, callback):
    after = mainloop._root.after

    def real_callback():
        # See bananagui.gui.timeouts.
        if callback() == add_timeout.RUN_AGAIN:
            after(milliseconds, real_callback)

    after(milliseconds, real_callback)
