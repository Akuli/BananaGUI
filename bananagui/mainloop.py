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
             |                          | call run()
             |                          V
             |       quit()        ,---------.
             `-------------------- | running |
                                   `---------'
                                   \____ ____/
                                        V
                                    the run()
                                    function
                                   is running

Note that :func:`bananagui.load` will call :func:`~init` by default and
most applications don't run the mainloop more than once, so usually you
don't need to worry about the "not initialized" state.
"""

import math
import sys
import traceback

from bananagui import _modules

__all__ = ['init', 'run', 'quit', 'add_timeout']


#class _DebugRoot(__import__('tkinter').Tk):
#    tk = None
#
#    def __init__(self):
#        super().__init__()
#        real_tk = self.tk
#
#        class _FakeTk:
#            def call(self, *args):
#                print(args)
#                return real_tk.call(*args)
#
#        tk = _FakeTk()
#        tk.__dict__.update({
#            name: getattr(self.tk, name)
#            for name in dir(self.tk)
#            if name != 'call'
#        })
#        self.tk = tk


class _TkinterLoop:

    def __init__(self):
        self._root = _modules.tk.Tk()
        #self._root = _DebugRoot()
        self._root.withdraw()    # hide it

    def run(self):
        self.running = True
        try:
            self._root.mainloop()
        finally:
            self.running = False

    def quit(self):
        self._root.destroy()

    def add_timeout(self, ms, callback):
        def real_callback():
            if callback():
                schedule()

        schedule = functools.partial(self._root.after, ms, real_callback)
        schedule()


_loop = None


def init():
    """Set up the mainloop.

    Note that :func:`bananagui.load_wrapper` runs this by default.
    """
    global _loop
    if _loop is not None:
        raise RuntimeError("the mainloop is already initialized")

    if _modules.name == 'tkinter':
        _loop = _TkinterLoop()
    else:
        raise NotImplementedError

    _loop.running = False
    _loop.error = None


def _check_initialized():
    if _loop is None:
        raise RuntimeError("the mainloop hasn't been initialized")


def run():
    """Run the mainloop until :func:`~quit` is called."""
    global _loop
    if _loop is None:
        raise RuntimeError("init() wasn't called")
    if _loop.running:
        raise RuntimeError("two mainloops cannot be ran at the same time")

    _loop.running = True
    try:
        _loop.run()
    finally:
        _loop.running = False

    if _loop.error is not None:
        raise _loop.error


def quit():
    """Make :func:`~run` return.

    Quitting when the main loop is not running does nothing.
    """
    if _loop is not None and _loop.running:
        _loop.quit()


def add_timeout(seconds, callback, *args):
    """Run ``callback(*args)`` after waiting.

    If the function returns :data:`bananagui.RUN_AGAIN` it will be
    called again after waiting again. Depending on the GUI toolkit, this
    may or may not work when the main loop is not running.

    The waiting time can be an integer or a float. It's not guaranteed
    to be exact, but it's good enough for most purposes. Use something
    like :func:`time.time` if you need to measure time in the callback
    function.

    Unlike in most other GUI toolkits, calling :func:`sys.exit` from a
    callback works.
    """
    if seconds <= 0:
        raise ValueError("timeouts need to be positive, not " + repr(seconds))
    milliseconds = math.ceil(seconds * 1000)

    if _loop is None:
        raise RuntimeError("init() wasn't called")
    if not _loop.running:
        raise RuntimeError("the mainloop isn't running")

    # last item in the stack trace is this frame, so before that
    add_timeout_call = traceback.format_stack()[-2]

    def real_callback():
        try:
            result = callback(*args)
            if result == bananagui.RUN_AGAIN:
                return True
            if result is None:
                return False
            raise ValueError("callback returned %r, expected None "
                             "or bananagui.RUN_AGAIN" % (result,))

        # allow using sys.exit() in callbacks
        except SystemExit as err:
            _loop.error = err
            _loop.quit()

        except Exception:
            # We can magically show where add_timeout() was called.
            lines = traceback.format_exception(*sys.exc_info())
            lines.insert(1, add_timeout_call)  # After 'Traceback (bla bla):'.
            sys.stderr.writelines(lines)
            return False     # Don't run again.

    _loop.add_timeout(real_callback)
