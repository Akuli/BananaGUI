"""Things that BananaGUI uses internally."""

import collections.abc
import contextlib
import sys
import traceback


def _type_name(cls):
    if cls.__module__ == 'builtins':
        # builtins.str -> str
        return cls.__name__
    if cls.__module__.startswith('bananagui.'):
        # bananagui._types.Callback -> bananagui.Callback
        return 'bananagui.' + cls.__name__
    return cls.__module__ + '.' + cls.__name__


class Callback:
    """An object like bindings in tkinter or signals in Qt and GTK+.

    You can connect functions to callbacks with the :meth:`connect`
    method, and they will be called when BananaGUI runs the callback.

    *argtypes* specifies the types of arguments that :meth:`run` and the
    connected functions will take. For example, a ``Callback(int, int)``
    can be ran like ``the_callback.run(1, 2)``, and it will run each
    connected function like ``function(1, 2)``.

    >>> cb = Callback(int, int)
    >>> cb
    bananagui.Callback(int, int)
    >>> cb.connect(print)
    >>> cb.run("lel")
    Traceback (most recent call last):
      ...
    TypeError: should be run(int, int), not run(str)
    >>> cb.run(1, 2)     # runs print(1, 2)
    1 2
    """

    def __init__(self, *argtypes):
        self._argtypes = argtypes
        self._blocklevel = 0

        # This could be an ordered dictionary to speed up is_connected()
        # and disconnect(), but speed isn't really an issue because
        # there's usually not many functions connected to a callback at
        # the same time. A dictionary would also add more limitations,
        # like requiring hashable callback functions and having each
        # function connected at most once. Simple is better than
        # complex.
        self._connections = []

    def __repr__(self):
        signature = ', '.join(map(_type_name, self._argtypes))
        return 'bananagui.Callback(%s)' % signature

    def connect(self, func, *extra_args):
        """Schedule a function to be called when the callback is ran.

        *extra_args* is a handy way to pass information to the callback
        function. There's no need to use lambda or :func:`functools.partial`.
        If the callback is ran with other arguments, they will be added
        before *extra_args*, like this::

            >>> cb = Callback(int)
            >>> cb.connect(print, "hello")
            >>> cb.run(123)     # 123 goes first
            123 hello

        .. note::
            :meth:`~is_connected` and :meth:`~disconnect` don't check
            anything about *extra_args*, so it's not possible to connect
            the same function with different *extra_args* and then undo
            different connections based on the *extra_args*.
        """
        stack_info = traceback.format_stack()[-2]   # whatever called this
        self._connections.append((func, extra_args, stack_info))

    def is_connected(self, func):
        """Check if :meth:`~connect` has been called with *func*."""
        for infotuple in self._connections:
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
        """Undo a :meth:`~connect` call."""
        for index, infotuple in enumerate(self._connections):
            if infotuple[0] == func:
                del self._connections[index]
                return
        raise ValueError("the function is not connected")

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

    def run(self, *args):
        """Run the connected functions as described in connect().

        This does nothing if code under a ``with the_callback.blocked()``
        is currently running somewhere. No exceptions are raised. If a
        callback raises an exception, this method handles it and prints
        the traceback to :data:`sys.stderr`.
        """
        if (len(args) != len(self._argtypes)
                or not all(map(isinstance, args, self._argtypes))):
            good = ', '.join(map(_type_name, self._argtypes))
            bad = ', '.join(_type_name(type(arg)) for arg in args)
            raise TypeError("should be run(%s), not run(%s)" % (good, bad))

        if self._blocklevel != 0:
            # It's blocked.
            return

        for func, extra_args, stack_info in self._connections:
            try:
                func(*(args + extra_args))
            except Exception as e:
                # We can magically show where this callback was connected.
                lines = traceback.format_exception(*sys.exc_info())
                lines.insert(1, stack_info)  # After 'Traceback (bla bla):'.
                sys.stderr.writelines(lines)
