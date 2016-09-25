"""Main loop."""

import sys

from bananagui import utils


class MainLoop:
    """A mainloop class.

    This is a class just because implementing this as a class was easier
    than implementing this as a function. You don't need to create an
    instance of this class to be able to use it.
    """

    _initialized = False
    _running = False

    @classmethod
    def init(cls):
        """Initialize the BananaGUI wrapper.

        Call this before calling anything else in the wrapper. You can
        call this multiple times.
        """
        if not cls._initialized:
            super().init()
            cls._initialized = True

    @classmethod
    def run(cls):
        """Run the mainloop until quit() is called.

        Return zero or None on success and a nonzero integer on failure,
        or raise an exception instead of returning.
        """
        assert cls._initialized, "initialize the mainloop before running it"
        assert not cls._running, "cannot run the mainloop twice"
        cls._running = True
        try:
            return super().run()
        finally:
            cls._running = False
            cls._initialized = False

    @classmethod
    def quit(cls):
        """Stop the mainloop started by main().

        Quitting when the main loop is not running does nothing.
        """
        if cls._running:
            super().quit()

    @utils.ClassProperty
    def running(cls):
        """Check if the mainloop is running."""
        return cls._running

    @utils.ClassProperty
    def initialized(cls):
        return cls._initialized
