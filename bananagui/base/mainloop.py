"""Main loop."""

import sys


class MainLoop:
    """A mainloop class.

    This is a class just because implementing this as a class was easier
    than implementing this as a function. You don't need to create an
    instance of this class to be able to use it.
    """

    __running = False

    @classmethod
    def init(cls, args=None):
        """Initialize the BananaGUI wrapper.

        Call this before calling anything else in the wrapper. You can
        call this multiple times.
        """
        if args is None:
            args = sys.argv
        super().init(args)

    @classmethod
    def run(cls):
        """Run the mainloop until quit() is called.

        Return an exit status or None.
        """
        cls.__running = True
        try:
            exit_status = super().run()
        except Exception as e:
            exit_status = 1
            raise e
        finally:
            cls.__running = False
        return exit_status

    @classmethod
    def quit(cls, *args):
        """Stop the mainloop started by main().

        This ignores all positional arguments. Quitting when the main
        loop is not running does nothing.
        """
        if cls.__running:
            super().quit()

    @classmethod
    def is_running(cls):
        """Check if the mainloop is running."""
        return cls.__running
