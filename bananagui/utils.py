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

"""BananaGUI's utility functions and other things."""

import importlib.util
import re


def all_equal(iterable):
    """Return True if all elements of iterable are equal.

    iterable must contain at least one element.

    >>> all_equal([1, 1.0])
    True
    >>> all_equal([1, 2])
    False
    """
    iterator = iter(iterable)
    first = next(iterator)
    for element in iterator:
        if element != first:
            return False
    return True


def common_beginning(*iterables):
    """Check how many common elements the beginnings of iterables have.

    >>> common_beginning([1, 2, 3, 4], [1, 2, 4, 3])
    2
    >>> common_beginning([2, 1, 3, 4], [1, 2, 3, 4])
    0
    """
    assert len(iterables) >= 2, "two iterables are needed for comparing"
    result = 0
    rows = iter(zip(*iterables))
    try:
        while all_equal(next(rows)):
            result += 1
    except StopIteration:
        pass
    return result


def find_attribute(attribute, *objects):
    """Get an attribute from any of objects.

    >>> class Thing:
    ...     pass
    ...
    >>> a = Thing()
    >>> b = Thing()
    >>> a.stuff = 'a stuff'
    >>> b.stuff = 'b stuff'
    >>> b.stuff2 = 'b stuff 2'
    >>> find_attribute('stuff', a, b)
    'a stuff'
    >>> find_attribute('stuff2', a, b)
    'b stuff 2'
    """
    for obj in objects:
        try:
            return getattr(obj, attribute)
        except AttributeError:
            pass
    raise AttributeError("none of the objects have an attribute %r"
                         % attribute)


def rangestep(range_object):
    """Return a range object's step.

    Unlike range_object.step, this also works on Python 3.2.

    >>> rangestep(range(10))
    1
    >>> rangestep(range(5, 10))
    1
    >>> rangestep(range(5, 10, 2))
    2
    """
    try:
        return range_object.step
    except AttributeError:
        if len(range_object) >= 2:
            # The range has enough items for calculating the step.
            return range_object[1] - range_object[0]
        # This hacky code only runs on Python 3.2.
        if repr(range_object).count(',') < 2:
            # The repr doesn't show the step, so it's the default.
            return 1
        # The repr shows the step so we can get it from that.
        match = re.search(r'(-?\d+)\)$', repr(range_object))
        return int(match.group(1))


# TODO: update the docstring.
def add_property(name, *, add_changed=False):
    """A handy way to add a property to a class.

    >>> class Base:
    ...     def set_test(self, test):
    ...         print("base sets test to", test)
    ...
    >>> @add_property('test', add_changed=True)
    ... class Thingy:
    ...     def __init__(self):
    ...         self.base = Base()
    ...         self._test = 'default test'
    ...     def run_callbacks(self, name):
    ...         # bananagui.widgets.Widget implements this.
    ...         for callback in getattr(self, name):
    ...             callback(self)
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

    A _set_NAME method will be called with the new value as an argument.
    This method may raise an exception if the value is invalid.
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
            getattr(self.base, 'set_' + name)(value)

            if add_changed:
                self.run_callbacks('on_%s_changed' % name)

        setattr(cls, name, property(getter, setter))

        if add_changed:
            def changed_getter(self):
                try:
                    return getattr(self, '_on_%s_changed' % name)
                except AttributeError:
                    setattr(self, '_on_%s_changed' % name, [])
                    return getattr(self, '_on_%s_changed' % name)

            setattr(cls, 'on_%s_changed' % name, property(changed_getter))

        return cls

    return inner


try:
    resolve_modulename = importlib.util.resolve_name
    import_module = importlib.import_module
except AttributeError:
    # Python 3.2, there is no importlib.util.resolve_name and
    # importlib.import_module doesn't import parent packages
    # automatically. This doctest also runs with 3.2 only.
    def resolve_modulename(modulename, package=None):
        """Like importlib.util.resolve_modulename, but for Python 3.2.

        >>> import sys
        >>> resolve_modulename('bananagui.bases.tkinter', 'whatever')
        'bananagui.bases.tkinter'
        >>> resolve_modulename('.tkinter', 'bananagui.bases')
        'bananagui.bases.tkinter'
        """
        if modulename.startswith('.'):
            if package is None:
                raise ValueError("a package is needed for %r" % (modulename,))
            while modulename.startswith('..'):
                # We need to go up one level and remove the dot that
                # represents it.
                package, junk = package.rsplit('.', 1)
                modulename = modulename[1:]
            # At this point there's still one dot left in modulename.
            modulename = package + modulename
        return modulename

    def import_module(modulename):
        """Import a module and its parent modules as needed."""
        current = []
        for part in modulename.split('.')[:-1]:
            # Loop through and import the parent modules.
            current.append(part)
            importlib.import_module('.'.join(current))
        return importlib.import_module(modulename)


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
