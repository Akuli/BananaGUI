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

"""The BananaGUI main loop."""

import warnings

import bananagui

_initialized = False
_running = False


def init():
    """Initialize the mainloop again after running it.

    You need this only if you want to run the mainloop multiple times.
    """
    global _initialized
    if _initialized:
        raise RuntimeError("the mainloop is initialized already")
    bananagui._get_wrapper('mainloop:init')()
    _initialized = True


def run():
    """Run the main loop until quit() is called."""
    global _initialized
    global _running
    if not _initialized:
        raise RuntimeError("init() wasn't called")
    if _running:
        raise RuntimeError("two mainloops cannot be ran at the same time")
    wrapperfunc = bananagui._get_wrapper('mainloop:run')
    _running = True
    try:
        wrapperfunc()
    finally:
        _running = False
        _initialized = False


def quit(*args):
    """Make run() return.

    Quitting when the main loop is not running does nothing. Positional
    arguments are ignored.
    """
    if _running:
        bananagui._get_wrapper('mainloop:quit')()


def add_timeout(milliseconds, callback, *args, **kwargs):
    """Run callback(*args, **kwargs) after waiting.

    If the function returns bananagui.RUN_AGAIN it will be called again
    after waiting again. Depending on the GUI toolkit, this may or may
    not work when the main loop is not running.

    The waiting time is not guaranteed to be exact, but it's good enough
    for most purposes. Use something like time.time() if you need to
    measure time in the callback function.
    """
    if not isinstance(milliseconds, int):
        raise TypeError("expected an integer, got %r" % (milliseconds,))
    if milliseconds <= 0:
        raise ValueError("non-positive timeout %d" % milliseconds)

    def real_callback():
        result = callback(*args, **kwargs)
        if result not in {None, bananagui.RUN_AGAIN}:
            warnings.warn("BananaGUI callback %r returned %r, expected "
                          "None or RUN_AGAIN" % (callback, result),
                          RuntimeWarning)
            result = None
        return result

    wrapperfunc = bananagui._get_wrapper('mainloop:add_timeout')
    wrapperfunc(milliseconds, real_callback)
