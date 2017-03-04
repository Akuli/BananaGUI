from gi.repository import GLib

import bananagui


_loop = None  # Make flake8 happy.


def init():
    # Gtk.main() cannot be interrupted with Ctrl+C.
    global _loop
    _loop = GLib.MainLoop()


def run():
    _loop.run()


def quit():
    _loop.quit()


def add_timeout(milliseconds, callback):
    def real_callback():
        return callback() == bananagui.RUN_AGAIN

    GLib.timeout_add(milliseconds, real_callback)
