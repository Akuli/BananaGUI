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


class BananaObject:
    """A base for classes that need something from a BananaGUI base.

    Subclasses of this class cannot be instantiated if a base hasn't
    been loaded with load().

    This class also implements callbacks. They are lists of functions
    that run_callbacks() runs. Most callbacks are called with the
    object as the only argument, but it's possible to run callbacks
    with more arguments than that.

    Some BananaGUI classes aren't subclasses of this class because they
    don't need a base or callbacks.
    """

    def __init__(self):
        if not hasattr(self, '_base'):
            # A subclass didn't override __init__ and define a _base.
            # Getting the base with _get_base() when load() hasn't been
            # called will raise an error, so we don't need to worry
            # about that here.
            raise TypeError("cannot create instances of %r directly, "
                            "instantiate a subclass instead"
                            % type(self).__name__)
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
        assert isinstance(callback_attribute, str)

        # This is important, we don't rely on an assertion here.
        if callback_attribute in self._blocked:
            raise ValueError("cannot block %r twice" % (callback_attribute,))

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


def add_property(name, *, add_changed=False):
    """A handy way to add a property to a class.

        >>> class Base:
        ...     def set_test(self, test):
        ...         print("base sets test to", test)
        ...
        >>> @add_property('test', add_changed=True)
        ... class Thingy(BananaObject):
        ...     def __init__(self):
        ...         self._base = Base()
        ...         self._test = 'default test'
        ...         super().__init__()
        ...     def __repr__(self):
        ...         return '<the thingy object>'
        ...     def _check_test(self, test):
        ...         assert isinstance(test, str)
        ...
        >>> thing = Thingy()
        >>> thing
        <the thingy object>
        >>> thing.test
        'default test'
        >>> thing.test = 'new test'
        base sets test to new test
        >>> thing.test = 'new test'  # does nothing
        >>>
        >>> def user_callback(arg):
        ...     print("callback called with arg", arg)
        ...
        >>> thing.on_test_changed.append(user_callback)
        >>> thing.test = 'even newer test'
        base sets test to even newer test
        callback called with arg <the thingy object>

    If the new value is equal to the old value, setting the property
    sets the _NAME attribute to the new value and doesn't do anything
    else.

    If add_changed is True, an on_NAME_changed list will be created and
    everything in it will be called when the value is set to a new
    value that is not equal to the old value. The callbacks will get
    the instance as an argument.

    A _base.set_NAME method will be called with the new value as an
    argument after checking the value with _check_NAME.
    """
    def inner(cls):
        def getter(self):
            return getattr(self, '_' + name)

        def setter(self, value):
            if getattr(self, '_' + name) == value:
                # Skip a bunch of things.
                setattr(self, '_' + name, value)
                return

            # This needs to be before the setattr() to make sure that
            # invalid values doesn't get setattr()ed.
            getattr(self, '_check_' + name)(value)

            # The setter can run this again, so we need to just
            # return and do nothing if it happens. That's why the
            # setattr is here first.
            setattr(self, '_' + name, value)
            getattr(self._base, 'set_' + name)(value)

            if add_changed:
                self.run_callbacks('on_%s_changed' % name)

        setattr(cls, name, property(getter, setter))

        if add_changed:
            def changed_getter(self):
                try:
                    return getattr(self, '__on_%s_changed' % name)
                except AttributeError:
                    setattr(self, '__on_%s_changed' % name, [])
                    return getattr(self, '__on_%s_changed' % name)

            setattr(cls, 'on_%s_changed' % name, property(changed_getter))

        return cls

    return inner


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
