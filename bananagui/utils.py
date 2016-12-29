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


# TODO: do we need this?
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


try:
    resolve_modulename = importlib.util.resolve_name
    import_module = importlib.import_module
except AttributeError:
    # Python 3.2, there is no importlib.util.resolve_name and
    # importlib.import_module doesn't import parent packages
    # automatically. This doctest also runs with 3.2 only.
    def resolve_modulename(modulename, package=None):
        """Like importlib.util.resolve_modulename, but for Python 3.2.

        >>> resolve_modulename('bananagui.wrappers.tkinter', 'whatever')
        'bananagui.wrappers.tkinter'
        >>> resolve_modulename('.tkinter', 'bananagui.wrappers')
        'bananagui.wrappers.tkinter'
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
