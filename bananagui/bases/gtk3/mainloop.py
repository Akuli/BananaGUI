from gi.repository import GLib

import bananagui


_loop = None


def init():
    # Gtk.main() cannot be interrupted with Ctrl+C.
    global _loop
    _loop = GLib.MainLoop()


def main():
    _loop.run()


def quit():
    global _loop
    _loop.quit()
    _loop = None


def add_timeout(milliseconds, callback):
    def real_callback():
        return callback() == bananagui.RUN_AGAIN

    GLib.timeout_add(milliseconds, real_callback)
