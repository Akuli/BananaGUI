"""Timeout class."""


class Timeout:
    """A class for adding timeouts."""

    RUN_AGAIN = 1 << 1  # Don't allow returning True.

    @classmethod
    def add_timeout(cls, milliseconds, callback, *arguments):
        """Add a timeout.

        After waiting the given number of milliseconds, the callback is
        called with the given arguments. Seconds can be a float or an
        integer. The timing may start when the main loop is started or
        before it.

        If the callback returns Timeout.RUN_AGAIN, it will be ran again
        after waiting again.

        The waiting time is not guaranteed to be exact, but it's good
        enough for most purposes. Use something like time.time() if you
        need to measure time in the callbacks.
        """
        # Provide an add_timeout class in the wrapper. Its callback
        # won't have extra arguments.
        assert isinstance(milliseconds, int)
        assert milliseconds > 0, "timeouts need to be positive"
        assert callable(callback)
        super().add_timeout(milliseconds, callback)
