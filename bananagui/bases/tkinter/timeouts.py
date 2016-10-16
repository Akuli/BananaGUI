import bananagui
from . import mainloop


def add_timeout(milliseconds, callback):
    after = mainloop.root.after

    def real_callback():
        if callback() == bananagui.RUN_AGAIN:
            after(milliseconds, real_callback)

    after(milliseconds, real_callback)
