from bananagui import RUN_AGAIN
from . import mainloop


def add_timeout(milliseconds, callback):
    after = mainloop.root.after

    def real_callback():
        if callback() == RUN_AGAIN:
            after(milliseconds, real_callback)

    after(milliseconds, real_callback)
