from gi.repository import GLib

import bananagui


def add_timeout(milliseconds, callback):
    def real_callback():
        return callback() == bananagui.RUN_AGAIN

    GLib.timeout_add(milliseconds, real_callback)
