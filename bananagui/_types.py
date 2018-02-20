import abc
import collections.abc
import contextlib
import sys
import traceback

import bananagui    # for checking what it exposes
from bananagui import _modules


class UpdatingObject:
    """An object for use with :class:`.UpdatingProperty`."""

    def needs_updating(self):
        """Return True if :meth:`Updating.Property` updaters should run.

        This always returns True by default. Widgets return False when
        the widget has not been rendered yet.
        """
        return True

    def update_everything(self):
        """Runs when the value of any :class:`.UpdatingProperty` changes.

        *property_name* is the ``name`` that was used when creating
        :class:`UpdatingProperty`.
        """
        for name, value in type(self).__dict__.items():     # lol
            if isinstance(value, UpdatingProperty):
                value._update(self)


class UpdatingProperty(property):
    """A property that runs an additional updater function after setting.

    Don't use the ``.fset`` attribute of UpdatingProperty objects; it
    should be considered an implementation detail.

    .. note::
        This class can be used only in :class:`UpdatingObject` subclasses.
    """

    def __init__(self, fget=None, fset=None, fdel=None, fupdate=None,
                 doc=None):
        if fset is not None:
            fset = self._make_setter(fset)
        if doc is None and fget is not None:
            doc = getattr(fget, '__doc__', None)

        super().__init__(fget, fset, fdel, doc)
        self.__doc__ = doc
        self.fupdate = fupdate

    def _update(self, instance):
        if instance.needs_updating() and self.fupdate is not None:
            self.fupdate(instance)

    def _make_setter(self, user_setter):
        # no need to use functools.wraps because setter docstrings and
        # other info are usually not used anywhere anyway
        def real_setter(instance, value):
            user_setter(instance, value)
            self._update(instance)

        real_setter._user_setter = user_setter
        return real_setter

    def _get_fset(self):
        if self.fset is None:
            return None
        return self.fset._user_setter

    def getter(self, fget):
        return UpdatingProperty(
            fget, self._get_fset(), self.fdel, self.fupdate, self.__doc__)

    def setter(self, fset):
        return UpdatingProperty(
            self.fget, fset, self.fdel, self.fupdate, self.__doc__)

    def deleter(self, fdel):
        return UpdatingProperty(
            self.fget, self._get_fset(), fdel, self.fupdate, self.__doc__)

    def updater(self, fupdate):
        """A decorator like ``@setter`` and ``@getter`` for the updater."""
        return UpdatingProperty(
            self.fget, self._get_fset(), self.fdel, fupdate, self.__doc__)

    @classmethod
    def updater_with_attr(cls, attrname, *, doc=None):
        """A convenient way to create a minimal property.

        This...

        .. code-block:: python

            class Thing(UpdatingObject):
                @UpdatingProperty.updater_with_attr('_stuff')
                def stuff():
                    ...update stuff...

        ...is equivalent to this::

            class Thing(UpdatingObject):

                @UpdatingProperty
                def stuff(self):
                    return self._stuff

                @stuff.setter
                def stuff(self, value):
                    self._stuff = value

                @stuff.updater
                def stuff(self, value):
                    ...update stuff...

        If the *name* argument not specified, it defaults to
        ``attrname.lstrip('_')``.
        """
        def fget(self):
            return getattr(self, attrname)

        def fset(self, value):
            setattr(self, attrname, value)

        def decorator(fupdate):
            if doc is None and fupdate.__doc__ is not None:
                the_doc = fupdate.__doc__
            else:
                the_doc = doc
            return cls(fget, fset, None, fupdate, the_doc)

        return decorator


def _get_class_name(cls):
    if cls.__module__ == 'builtins':
        # builtins.str -> str
        return cls.__name__
    if (cls.__module__.startswith('bananagui.') and
            getattr(bananagui, cls.__name__, None) is cls):
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
        signature = ', '.join(map(_get_class_name, self._argtypes))
        return '%s(%s)' % (_get_class_name(type(self)), signature)

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
        """Run the connected functions.

        This does nothing if code under a ``with the_callback.blocked()``
        is currently running somewhere. No exceptions are raised. If a
        callback raises an exception, this method handles it and prints
        the traceback to :data:`sys.stderr`.
        """
        if (len(args) != len(self._argtypes)
                or not all(map(isinstance, args, self._argtypes))):
            good = ', '.join(map(_get_class_name, self._argtypes))
            bad = ', '.join(map(_get_class_name, map(type, args)))
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
