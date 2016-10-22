# Copyright (c) 2016 Akuli

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Main loop."""

import warnings

import bananagui
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


def add_timeout(milliseconds: int, callback, *args, **kwargs) -> None:
    """Run callback(*args, **kwargs) after waiting.

    If the function returns RUN_AGAIN it will be called again after
    waiting again. Depending on the GUI toolkit, the timing may start
    when bananagui.main() is started or before it.

    The waiting time is not guaranteed to be exact, but it's good enough
    for most purposes. Use something like time.time() if you need to
    measure time in the callback function.
    """
    assert milliseconds > 0, "non-positive timeout %r" % (milliseconds,)
    assert callable(callback), "non-callable callback"

    def real_callback():
        result = callback(*args, **kwargs)
        if result not in {None, bananagui.RUN_AGAIN}:
            warnings.warn("BananaGUI callback returned %r, expected "
                          "None or bananagui.RUN_AGAIN" % (result,),
                          RuntimeWarning)
            result = None
        return result

    _base.add_timeout(milliseconds, real_callback)
