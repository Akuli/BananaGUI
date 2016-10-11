from gi.repository import GLib
from bananagui import RUN_AGAIN


def add_timeout(milliseconds, callback):
    def real_callback():
        return callback() == RUN_AGAIN

    GLib.timeout_add(milliseconds, real_callback)
