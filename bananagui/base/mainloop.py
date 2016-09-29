"""Main loop."""

import sys

from bananagui import utils


class MainLoop:
    """A mainloop class.

    This is a class just because implementing this as a class is easier
    than implementing this as a function. You don't need to create an
    instance of this class to be able to use it.

    bananagui.load() calls MainLoop.init(), bananagui.main() calls
    MainLoop.run() and bananagui.quit() calls MainLoop.quit(). In most
    cases it's recommended to use these functions instead of calling
    methods from MainLoop directly.
    """

    initialized = False
    running = False

    @classmethod
    def init(cls):
        """Initialize the BananaGUI wrapper.

        Call this before calling anything else in the wrapper. You can
        call this multiple times.
        """
        if not cls.initialized:
            super().init()
            cls.initialized = True

    @classmethod
    def run(cls):
        """Run the mainloop until quit() is called.

        Return zero or None on success and a nonzero integer on failure,
        or raise an exception instead of returning.
        """
        assert cls.initialized
        assert not cls.running
        cls.running = True
        try:
            return super().run()
        finally:
            cls.running = False
            cls.initialized = False

    @classmethod
    def quit(cls):
        """Stop the mainloop started by main().

        Quitting when the main loop is not running does nothing.
        """
        if cls.running:
            super().quit()
