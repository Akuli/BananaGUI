# Copyright (c) 2016-2017 Akuli

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

"""Things that BananaGUI uses internally."""

import contextlib
import sys
import traceback
try:
    import collections.abc as abcoll
except ImportError:     # pragma: no cover
    # Python 3.2, no separate collections.abc.
    import collections as abcoll

__all__ = ['add_property', 'add_callback']


class _Callback:
    """An object like bindings in tkinter or signals in Qt and GTK+.

    You can connect functions to callbacks with the connect() method,
    and they will be called when BananaGUI runs the callback.
    """

    def __init__(self, obj, name):
        self._object = obj
        self._name = name
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
        cls = type(self._object)
        return '<BananaGUI callback %r of %s.%s object>' % (
            self._name, cls.__module__, cls.__name__)

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
            #   >>> t.stuff is t.stuff
            #   False
            #   >>> t.stuff == t.stuff
            #   True
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

        Use this as a context manager.
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
                lines = traceback.format_exception(
                    type(e), e, e.__traceback__)
                lines.insert(1, stack_info)  # After 'Traceback (bla bla):'.
                sys.stderr.writelines(lines)


def add_property(name, *, add_changed=False, allow_none=False,
                 type=object, how_many=1, minimum=None, maximum=None,
                 choices=None, extra_setter=None, doc=None):
    """A handy way to add a property to a class.

    >>> class Wrapper:
    ...     def set_test(self, test):
    ...         print("wrapper sets test to", test)
    ...
    >>> @add_property('test', add_changed=True, type=str)
    ... class Thingy:
    ...     def __init__(self):
    ...         self._wrapper = Wrapper()
    ...         self._prop_test = 'default test'
    ...
    >>> thing = Thingy()
    >>> thing.test
    'default test'
    >>> thing.test = 'new test'
    wrapper sets test to new test
    >>> thing.test = 'new test'  # does nothing
    >>> thing.test = 123
    Traceback (most recent call last):
      ...
    TypeError: test needs a value of type str, not 123
    >>>
    >>> def user_callback():
    ...     print("user callback runs")
    ...
    >>> thing.on_test_changed.connect(user_callback)
    >>> thing.test = 'even newer test'
    wrapper sets test to even newer test
    user callback runs
    >>>

    If the new value is equal to the old value, setting the property
    sets the _NAME attribute to the new value and doesn't do anything
    else.

    If add_changed is True, an on_NAME_changed callback will be added.
    It will be ran when the value is set to a new value that is not
    equal to the old value.

    Other arguments will be used for checking the value, and the
    extra_setter will be called with the instance and new value as
    arguments after the checking. It may raise an exception if the
    value is invalid.

    A _wrapper.set_NAME method will be called with the new value as an
    argument after checking the value and possibly calling extra_setter.
    """
    def getter(self):
        return getattr(self, '_prop_' + name)

    def setter(self, new_value):
        if getattr(self, '_prop_' + name) == new_value:
            # Skip a bunch of things.
            setattr(self, '_prop_' + name, new_value)
            return

        # This needs to be before the setattr() to make sure that
        # invalid values doesn't get setattr()ed.
        if how_many == 1:
            values2check = [new_value]
        else:
            # We don't want to allow iterators or sets because the
            # values need to be iterated over multiple times and they
            # need to be consistent.
            if isinstance(new_value, abcoll.Set):
                raise TypeError("%s value needs to be a sequence, not %r"
                                % (name, new_value))
            if len(new_value) != how_many:
                raise ValueError("%s value needs to be of length %d, got %r"
                                 % (name, how_many, new_value))
            values2check = new_value

        for value in values2check:
            if value is None:
                if not allow_none:
                    raise ValueError("None is not allowed")
            else:
                if not isinstance(value, type):
                    raise TypeError("%s needs a value of type %s, not %r"
                                    % (name, type.__name__, value))
                if choices is not None and value not in choices:
                    raise ValueError("invalid %s value %r, not in %r"
                                     % (name, value, choices))
                if minimum is not None and value < minimum:
                    raise ValueError(
                        "%s value %r is too small, needs to be >= %r"
                        % (name, value, minimum))
                if maximum is not None and value > maximum:
                    raise ValueError(
                        "%s value %r is too big, needs to be <= %r"
                        % (name, value, maximum))
        if extra_setter is not None:
            extra_setter(self, new_value)

        # The setter can run this again, so we need to just
        # return and do nothing if it happens. That's why the
        # setattr is here first.
        setattr(self, '_prop_' + name, new_value)
        getattr(self._wrapper, 'set_' + name)(new_value)

        if add_changed:
            getattr(self, 'on_%s_changed' % name).run()

    def inner(cls):
        setattr(cls, name, property(getter, setter, doc=doc))
        if add_changed:
            callbackdoc = "This callback is ran when %s changes." % name
            add_callback('on_%s_changed' % name, doc=callbackdoc)(cls)
        return cls

    return inner


def add_callback(name, *, doc=None):
    """Add a callback to a class easily.

    Use this as a decorator.

    >>> @add_callback('on_stuff')
    ... class Thing:
    ...     pass
    ...
    >>> t = Thing()
    >>> t.on_stuff.connect(print, "arg1", "arg2", "arg3")
    >>> t.on_stuff.run()
    arg1 arg2 arg3
    >>>
    """
    def getter(self):
        try:
            return getattr(self, '__callback_' + name)
        except AttributeError:
            setattr(self, '__callback_' + name, _Callback(self, name))
            return getattr(self, '__callback_' + name)

    def inner(cls):
        setattr(cls, name, property(getter, doc=doc))
        return cls

    return inner
