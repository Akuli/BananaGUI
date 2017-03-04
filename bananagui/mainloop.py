r"""This module provides access to the GUI toolkit's mainloop.

The mainloop can be in three different states:

* **Not initialized:** The mainloop is doing nothing, and it's not ready
  to run. This is the current state when this module has just been
  imported for the first time.
* **Initialized:** Now the mainloop is ready to run, but it's not running
  yet. Widgets can be created and timeouts can be added, but the
  timeouts aren't guaranteed to run and the widgets aren't guaranteed to
  be visible yet. Typically the mainloop is in this state for a short
  time while the widgets are being created.
* **Running:** Now the mainloop is running. Widgets are visible and
  timeouts run. New widgets can be still made and new timeouts can be
  added. Applications are in this state most of the time.

Different functions in this module can be used for going from one state
to another:

.. code-block:: none

   ,-----------------.  init()  ,-------------.
   | not initialized | -------> | initialized |
   `-----------------'          `-------------'
           /|\                         |
            |               quit()     | call run()
            |                  \       V
            |                   \ ,---------.
            `-------------------- | running |
                                  `---------'
                                  \____ ____/
                                       V
                                   the run()
                                   function
                                  is running

Note that :func:`bananagui.load_wrapper` will call :func:`~init` by
default and most applications don't run the mainloop more than once, so
usually you don't need to worry about the "Not initialized" state.
"""

import math
import sys
import traceback

import bananagui

__all__ = ['init', 'run', 'quit', 'add_timeout']

_initialized = False
_running = False


def init():
    """Set up the mainloop.

    Note that :func:`bananagui.load_wrapper` runs this by default.
    """
    global _initialized
    if _initialized:
        raise RuntimeError("the mainloop is initialized already")
    bananagui._get_wrapper('mainloop:init')()
    _initialized = True


def run():
    """Run the mainloop until :func:`~quit` is called."""
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


def quit():
    """Make :func:`~run` return.

    Quitting when the main loop is not running does nothing.
    """
    if _running:
        bananagui._get_wrapper('mainloop:quit')()


def add_timeout(seconds, callback, *args):
    """Run ``callback(*args)`` after waiting.

    If the function returns :data:`bananagui.RUN_AGAIN` it will be
    called again after waiting again. Depending on the GUI toolkit, this
    may or may not work when the main loop is not running.

    The waiting time is not guaranteed to be exact, but it's good enough
    for most purposes. Use something like :func:`time.time` if you need
    to measure time in the callback function.
    """
    if seconds <= 0:
        raise ValueError("non-positive timeout %s" % (seconds,))
    milliseconds = math.ceil(seconds * 1000)

    add_timeout_call = traceback.format_stack()[-2]

    def real_callback():
        try:
            result = callback(*args)
            if result not in {None, bananagui.RUN_AGAIN}:
                raise ValueError("callback returned %r, expected None "
                                 "or bananagui.RUN_AGAIN" % (result,))
        except Exception as e:
            # We can magically show where add_timeout() was called.
            lines = traceback.format_exception(type(e), e, e.__traceback__)
            lines.insert(1, add_timeout_call)  # After 'Traceback (bla bla):'.
            sys.stderr.writelines(lines)
            return None     # Don't run again.
        return result

    wrapperfunc = bananagui._get_wrapper('mainloop:add_timeout')
    wrapperfunc(milliseconds, real_callback)
