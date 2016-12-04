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

_base = bananagui._get_base('mainloop')

_initialized = True
_running = False


def reinitialize():
    """Initialize the mainloop again after running it.

    You need this only if you want to run the mainloop multiple times.
    """
    global _initialized
    assert not _initialized, "the mainloop is initialized already"
    _base.reinitialize()
    _initialized = True


def run():
    """Run the main loop until quit() is called."""
    global _initialized
    global _running
    assert _initialized, "use reinitialize()"
    assert not _running, "two mainloops cannot be ran at the same time"
    _running = True
    try:
        _base.run()
    finally:
        _running = False
        _initialized = False


def quit(*args):
    """Make run() return.

    Quitting when the main loop is not running does nothing. Positional
    arguments are ignored.
    """
    if _running:
        _base.quit()


def add_timeout(milliseconds, callback, *args, **kwargs):
    """Run callback(*args, **kwargs) after waiting.

    If the function returns bananagui.RUN_AGAIN it will be called again
    after waiting again. Depending on the GUI toolkit, this may or may
    not work when the main loop is not running.

    The waiting time is not guaranteed to be exact, but it's good enough
    for most purposes. Use something like time.time() if you need to
    measure time in the callback function.
    """
    # Someone might pass a float time and this would fail randomly with
    # some GUI toolkits.
    assert isinstance(milliseconds, int)
    assert milliseconds > 0

    def real_callback():
        result = callback(*args, **kwargs)
        if result not in {None, bananagui.RUN_AGAIN}:
            warnings.warn("BananaGUI callback %r returned %r, expected "
                          "None or RUN_AGAIN" % (callback, result),
                          RuntimeWarning)
            result = None
        return result

    _base.add_timeout(milliseconds, real_callback)
