from . import mainloop


def add_timeout(milliseconds, callback):
    after = mainloop.root.after

    def real_callback():
        if callback() == add_timeout.RUN_AGAIN:  # See bananagui.gui.timeouts.
            after(milliseconds, real_callback)

    after(milliseconds, real_callback)
