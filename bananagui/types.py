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

"""Things that BananaGUI uses internally."""

import contextlib
import itertools
import traceback


class Callback:
    """An object like signals in Qt GTK+ and bindings in tkinter.

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
        objrepr = repr(self._object)
        if objrepr.startswith('<') and objrepr.endswith('>'):
            objrepr = objrepr[1:-1]
        return '<BananaGUI callback %r of %s>' % (self._name, objrepr)

    def connect(self, func, *args):
        """Schedule a function to be called when the callback is ran.

        The function will get the object this callback belongs to as
        its first argument, and *extra_args as other arguments. This is
        a handy way to pass information to the callbacks, there's no
        need to use lambda or functools.partial().
        """
        stack_info = traceback.format_stack()[-2]  # The connect() call.
        self._callbacks.append((func, args, stack_info))

    def is_connected(self, func):
        """Check if connect() has been called with func as an argument."""
        for infotuple in self._callbacks:
            if infotuple[0] is func:
                return True
        return False

    def disconnect(self, func):
        """Undo a connect() call."""
        for index, infotuple in enumerate(self._callbacks):
            if infotuple[0] is func:
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
        is currently running. Return True if everything succeeded and no
        exceptions were raised, and False if an exception was raised
        (and handled).
        """
        if self._blocklevel != 0:
            # It's blocked.
            return True
        for func, args, stack_info in self._callbacks:
            try:
                func(self._object, *args)
            except Exception as e:
                # We can magically show where this callback was connected.
                lines = traceback.format_exception(
                    type(e), e, e.__traceback__)
                lines.insert(1, stack_info)  # After 'Traceback (bla bla):'.
                sys.stderr.writelines(lines)
                return False
        return True


class BananaObject:
    """A base for classes that need something from a BananaGUI wrapper.

    Subclasses of this class cannot be instantiated if a wrapper hasn't
    been loaded with load().

    This class also implements callbacks. They are lists of functions
    that run_callbacks() runs. Most callbacks are called with the
    object as the only argument, but it's possible to run callbacks
    with more arguments than that.

    Some BananaGUI classes aren't subclasses of this class because they
    don't need a wrapper or callbacks.
    """

    def __init__(self):
        if not hasattr(self, '_wrapper'):
            # A subclass didn't override __init__ and define a _wrapper.
            # Getting the wrapper with _get_wrapper() when bananagui.load()
            # hasn't been called will raise an error, so we don't need
            # to worry about that here.
            cls = type(self)
            raise TypeError("cannot create instances of %s.%s directly, "
                            "instantiate a subclass instead"
                            % (cls.__module__, cls.__name__))
        self._blocked = set()

    def __repr__(self):
        """Provide an informative string representation.

        The return value is constructed from the module and name of the
        class and the return value of _repr_parts. This method should
        return a list of things that will be joined with a comma to
        create the __repr__. The default __repr__ is used if
        _repr_parts returns an empty list.

        It's recommended to do something like this in _repr_parts:

            def _repr_parts(self):
                return ['thing=stuff'] + super()._repr_parts()
        """
        parts = self._repr_parts()
        if not parts:
            return super().__repr__()
        cls = type(self)
        return '<%s.%s object, %s>' % (
            cls.__module__, cls.__name__, ', '.join(parts))

    def _repr_parts(self):
        """Return an empty list to make super() usage easier.

        See also __repr__.
        """
        return []

    @contextlib.contextmanager
    def block(self, callback_attribute):
        """Prevent callbacks from running temporarily.

        Blocking is instance-specific.
        """
        if not isinstance(callback_attribute, str):
            raise TypeError("invalid attribute name %r"
                            % (callback_attribute,))
        if callback_attribute in self._blocked:
            raise RuntimeError("cannot block %r twice"
                               % (callback_attribute,))

        self._blocked.add(callback_attribute)
        try:
            yield
        finally:
            self._blocked.remove(callback_attribute)

    def run_callbacks(self, callback_attribute, *extra_args):
        """Run each callback in self.CALLBACK_ATTRIBUTE.

        This does nothing if the callback is blocked. The callbacks are
        ran with the widget and extra_args as arguments.
        """
        if callback_attribute not in self._blocked:
            for callback in getattr(self, callback_attribute):
                callback(self, *extra_args)


# TODO: Use _prop_NAME instead of _NAME?
def add_property(name, *, add_changed=False, allow_none=False,
                 type=object, how_many=1, minimum=None, maximum=None,
                 choices=None, extra_setter=None):
    """A handy way to add a property to a class.

    >>> class Wrapper:
    ...     def set_test(self, test):
    ...         print("wrapper sets test to", test)
    ...
    >>> @add_property('test', add_changed=True, type=str)
    ... class Thingy(BananaObject):
    ...     def __init__(self):
    ...         self._wrapper = Wrapper()
    ...         self._test = 'default test'
    ...         super().__init__()
    ...     def __repr__(self):
    ...         return '<the thingy object>'
    ...
    >>> Thingy.test     # doctest: +ELLIPSIS
    <property object at 0x...>
    >>> thing = Thingy()
    >>> thing
    <the thingy object>
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
    >>> def user_callback(arg):
    ...     print("callback called with arg", arg)
    ...
    >>> thing.on_test_changed.append(user_callback)
    >>> thing.test = 'even newer test'
    wrapper sets test to even newer test
    callback called with arg <the thingy object>
    >>>

    If the new value is equal to the old value, setting the property
    sets the _NAME attribute to the new value and doesn't do anything
    else.

    If add_changed is True, an on_NAME_changed list will be created and
    everything in it will be called when the value is set to a new
    value that is not equal to the old value. The callbacks will get
    the instance as an argument.

    The property's docstring will be doc. Other arguments will be used
    for checking the value, and the extra_setter will be called after
    the checking. It may raise an exception if the value is invalid.

    A _wrapper.set_NAME method will be called with the new value as an
    argument after checking the value.
    """
    def getter(self):
        return getattr(self, '_' + name)

    def setter(self, new_value):
        if getattr(self, '_' + name) == new_value:
            # Skip a bunch of things.
            setattr(self, '_' + name, new_value)
            return

        # This needs to be before the setattr() to make sure that
        # invalid values doesn't get setattr()ed.
        if how_many == 1:
            values2check = [new_value]
        else:
            # We don't want to allow iterators because the values
            # need to be iterated over multiple times. That's why a
            # len() check is good.
            if len(new_value) != how_many:
                raise TypeError("expected a sequence of length %d, got %r"
                                % (how_many, new_value))
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
        setattr(self, '_' + name, new_value)
        getattr(self._wrapper, 'set_' + name)(new_value)

        if add_changed:
            self.run_callbacks('on_%s_changed' % name)

    def inner(cls):
        setattr(cls, name, property(getter, setter))

        if add_changed:
            def changed_getter(self):
                try:
                    return getattr(self, '__on_%s_changed' % name)
                except AttributeError:
                    setattr(self, '__on_%s_changed' % name, [])
                    return getattr(self, '__on_%s_changed' % name)

            changed_getter.__doc__ = (
                "List of callbacks that are ran "
                "when the value of %r changes." % name)
            setattr(cls, 'on_%s_changed' % name, property(changed_getter))

        return cls

    return inner


def add_callback(name):
    """Add a callback to a class easily.

    Use this as a decorator.

    >>> @add_callback('on_stuff')
    ... class Thing:
    ...     def __repr__(self):
    ...         return '<the Thing object>'
    ... 
    >>> t = Thing()
    >>> t
    <the Thing object>
    >>> t.on_stuff
    <BananaGUI callback 'on_stuff' of the Thing object>
    >>> t.on_stuff.connect(print, "arg1", "arg2", "arg3")
    >>> success = t.on_stuff.run()
    <the Thing object> arg1 arg2 arg3
    >>> success
    True
    >>>
    """
    def getter(self):
        try:
            return getattr(self, '__callback_' + name)
        except AttributeError:
            setattr(self, '__callback_' + name, Callback(self, name))
            return getattr(self, '__callback_' + name)

    def inner(cls):
        setattr(cls, name, property(getter))
        return cls

    return inner
