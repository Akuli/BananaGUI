"""Main loop."""

from bananagui import _base


_initialized = False
_running = False


def init():
    """Initialize bananagui.gui.

    This is called automatically when bananagui.gui is imported for the
    first time.
    """
    # TODO: Take arguments here?
    global _initialized
    if not _initialized:
        _base.init()
        _initialized = True


def main():
    """Run bananagui.gui's mainloop until quit() is called.

    Raise an exception on failure.
    """
    global _initialized
    global _running
    assert _initialized, "init() wasn't called before calling main()"
    assert not _running, "two mainloops cannot be running at the same time"
    _running = True
    try:
        _base.main()
    finally:
        _running = False
        _initialized = False


def quit(*args):
    """Stop the mainloop started by main().

    All positional arguments are ignored. Quitting when the main loop is
    not running does nothing.
    """
    if _running:
        _base.quit()
