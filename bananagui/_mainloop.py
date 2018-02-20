# TODO: support running the mainloop multiple times?

import math
import sys
import threading
import time
import traceback

from bananagui import _modules


RUN_AGAIN = object()


class _DummyLoop:

    def __init__(self):
        self._done = threading.Event()

    def run(self):
        self._done.wait()

    def quit(self):
        self._done.set()

    def add_timeout(self, ms, callback):
        def real_callback():
            time.sleep(ms / 1000)
            while callback():
                time.sleep(ms / 1000)

        threading.Thread(target=real_callback).start()


class _TkinterLoop:

    def __init__(self):
        self._root = _modules.tk.Tk()
        self._root.withdraw()    # hide it

    def run(self):
        self._root.mainloop()

    def quit(self):
        self._root.destroy()

    def add_timeout(self, ms, callback):
        def real_callback():
            if callback():
                schedule()

        schedule = functools.partial(self._root.after, ms, real_callback)
        schedule()


class _GLibLoop:

    # this looks kind of java... lol
    def __init__(self):
        self._loop = _modules.GLib.MainLoop()

    def run(self):
        self._loop.run()

    def quit(self):
        self._loop.quit()

    def add_timeout(self, ms, callback):
        _modules.GLib.timeout_add(ms, callback)


_loop = None


def init():
    global _loop
    assert _loop is None, "_mainloop.init() was called twice"

    if _modules.name == 'tkinter':
        _loop = _TkinterLoop()
    elif _modules.name.startswith('gtk'):
        _loop = _GLibLoop()
    elif _modules.name == 'dummy':
        _loop = _DummyLoop()
    else:
        raise NotImplementedError

    _loop.running = False
    _loop.error = None


def _check_initialized():
    if _loop is None:
        raise RuntimeError("the mainloop hasn't been initialized")


def run():
    """Run the mainloop until :func:`bananagui.quit` is called."""
    global _loop
    if _loop is None:
        raise RuntimeError("init() wasn't called")
    if _loop.running:
        raise RuntimeError("two mainloops cannot be ran at the same time")

    _loop.running = True    # for quit()
    try:
        _loop.run()
        if _loop.error is not None:
            raise _loop.error
    finally:
        _loop.running = False
        _loop = None


def quit():
    """Make :func:`bananagui.run` return.

    Quitting when the main loop is not running does nothing.
    """
    if _loop is not None and _loop.running:
        _loop.quit()


def add_timeout(seconds, callback, *args):
    """Run ``callback(*args)`` after the given number of seconds.

    If the function returns :data:`bananagui.RUN_AGAIN` it will be
    called again after waiting again.

    The waiting time can be an integer or a float. It's not guaranteed
    to be exact, but it's good enough for most purposes. Use something
    like :func:`time.time` if you need to measure time in the callback
    function.

    Callbacks may call :func:`sys.exit`; :func:`bananagui.quit` will be
    called and :func:`bananagui.run` will then exit Python.
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
            if result is bananagui.RUN_AGAIN:
                return True
            if result is None:
                return False
            raise ValueError("callback returned %r, expected None "
                             "or bananagui.RUN_AGAIN" % (result,))

        # TODO: does it make sense to catch KeyboardInterrupt?

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
