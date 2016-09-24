"""Timeout class."""


class Timeout:
    """A class for adding timeouts."""

    RUN_AGAIN = 1

    @classmethod
    def add_timeout(cls, seconds, callback):
        """Add a timeout.

        After waiting the given number of seconds, the callback is
        called with no arguments. Seconds can be a float or an integer.
        The timing may start when the main loop is started or before it.

        If the callback returns Timeout.RUN_AGAIN, it will be ran again
        after waiting again.

        The waiting time is not guaranteed to be exact, but it's good
        enough for most purposes. Use something like time.time() if you
        need to measure time in the callbacks.
        """
        if not isinstance(seconds, (int, float)):
            raise TypeError("expected an integer or a float, got %r"
                            % (seconds,))
        if not callable(callback):
            raise TypeError("the callback must be callable")
        super().add_timeout(seconds, callback)
