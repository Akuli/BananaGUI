from gi.repository import GLib


def add_timeout(milliseconds, callback):

    milliseconds = int(seconds * 1000)
    def real_callback():
        # See bananagui.gui.timeouts.
        return callback() == add_timeout.RUN_AGAIN

    GLib.timeout_add(milliseconds, real_callback)
