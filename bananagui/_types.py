"""Things that BananaGUI uses internally."""

import collections.abc
import contextlib
import sys
import traceback

__all__ = ['Callback']


class Callback:
    """An object like bindings in tkinter or signals in Qt and GTK+.

    You can connect functions to callbacks with the ``connect()``
    method, and they will be called when BananaGUI runs the callback.

    If *repr_info* is given, it will be used to provide a useful
    ``__repr__``.
    """

    def __init__(self, repr_info=None):
        if repr_info is None:
            repr_info = 'at %#x' % id(self)
        self._repr_info = repr_info
        self._blocklevel = 0

        # This could be an ordered dictionary to speed up is_connected()
        # and disconnect(), but speed isn't really an issue because
        # there's usually not many functions connected to a callback at
        # the same time. A dictionary would also add more limitations,
        # like requiring hashable callback functions and having each
        # function connected at most once. Simple is better than
        # complex.
        self._callbacks = []

    def __repr__(self):
        return '<BananaGUI Callback %s>' % self._repr_info

    def connect(self, func, *args):
        """Schedule func(*args) to be called when the callback is ran.

        Passing arguments to this function is a handy way to pass
        information to the callback function. There's no need to use
        lambda or functools.partial().
        """
        stack_info = traceback.format_stack()[-2]  # The connect() call.
        self._callbacks.append((func, args, stack_info))

    def is_connected(self, func):
        """Check if connect() has been called with func as an argument."""
        for infotuple in self._callbacks:
            # It's important NOT to use is here because.. well...
            #   >>> class Thing:
            #   ...     def stuff(self):
            #   ...         pass
            #   ...
            #   >>> t = Thing()
            #   >>> t.stuff == t.stuff
            #   True
            #   >>> t.stuff is t.stuff
            #   False
            #   >>>
            if infotuple[0] == func:
                return True
        return False

    def disconnect(self, func):
        """Undo a connect() call."""
        for index, infotuple in enumerate(self._callbacks):
            if infotuple[0] == func:
                del self._callbacks[index]
                return
        raise ValueError("function is not connected")

    @contextlib.contextmanager
    def blocked(self):
        """Block this callback from running temporarily.

        Use this as a context manager. Calls to this may be nested.
        """
        self._blocklevel += 1
        try:
            yield
        finally:
            self._blocklevel -= 1

    def run(self):
        """Run the connected functions as described in connect().

        This does nothing if code under a `with this_callback.blocked():`
        is currently running. No exceptions are raised. If a callback
        raises an exception, this method handles it and prints the
        traceback to sys.stderr.
        """
        if self._blocklevel != 0:
            # It's blocked.
            return
        for func, args, stack_info in self._callbacks:
            try:
                func(*args)
            except Exception as e:
                # We can magically show where this callback was connected.
                lines = traceback.format_exception(*sys.exc_info())
                lines.insert(1, stack_info)  # After 'Traceback (bla bla):'.
                sys.stderr.writelines(lines)
