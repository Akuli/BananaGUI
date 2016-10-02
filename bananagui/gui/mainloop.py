"""Main loop."""

import sys

from bananagui import _base


initialized = False
running = False


def init():
    """Initialize bananagui.gui.

    This is called automatically when bananagui.gui is imported for the
    first time.
    """
    global initialized
    if not initialized:
        _base.init()
        initialized = True


def main():
    """Run bananagui.gui's mainloop until quit() is called.

    Raise an exception on failure.
    """
    global initialized
    global running
    assert initialized, "init() wasn't called before calling main()"
    assert not running, "two mainloops cannot be running at the same time"
    running = True
    try:
        _base.main()
    finally:
        running = False
        initialized = False


def quit(*args):
    """Stop the mainloop started by main().

    All positional arguments are ignored. Quitting when the main loop is
    not running does nothing.
    """
    if running:
        _base.quit()
