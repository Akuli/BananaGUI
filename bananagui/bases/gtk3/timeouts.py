from gi.repository import GLib


class Timeout:

    @classmethod
    def add_timeout(cls, seconds, callback):
        milliseconds = int(seconds * 1000)
        def real_callback():
            return callback() == cls.RUN_AGAIN

        GLib.timeout_add(milliseconds, real_callback)
