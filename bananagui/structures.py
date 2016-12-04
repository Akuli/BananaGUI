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

"""Handy classes for BananaGUI."""

import collections
import functools
import traceback
import warnings

try:
    from types import SimpleNamespace as NamespaceBase  # noqa
    from collections import abcoll
except ImportError:
    # types.SimpleNamespace and collections.abc are new in Python 3.3.
    from argparse import Namespace as NamespaceBase  # noqa
    abcoll = collections

from bananagui import utils


class _CallbackBase:
    """A mutable object that calls callbacks when it's mutated.

    The callbacks can be anything callable and they're stored in a
    _callbacks attribute. They will be called with the CallbackList as
    the only argument.
    """

    __slots__ = ('_data', '_callbacks')
    __hash__ = None

    def __init__(self, *args, **kwargs):
        self._data = type(self)._basetype(*args, **kwargs)
        self._callbacks = []

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self._data)

    @classmethod
    def _expose(cls, name):
        """Add a function to cls that exposes a self._data method."""
        function = getattr(cls._basetype, name)

        @functools.wraps(function)
        def exposer(self, *args, **kwargs):
            # We can't use self._data.copy() because lists don't have a
            # copy method on Python 3.2.
            old_data = cls._basetype(self._data)
            result = function(self._data, *args, **kwargs)
            new_data = cls._basetype(self._data)

            if old_data != new_data:
                # It has been mutated.
                try:
                    for callback in self._callbacks:
                        callback(old_data, new_data)
                except Exception as e:
                    # A callback doesn't like the new data. Let's
                    # restore it back to what it was before and reraise
                    # the exception.
                    self._data = old_data
                    raise e

            return result

        setattr(cls, name, exposer)

    @classmethod
    def _expose_all(cls, names):
        """Call cls._expose with each name.

        Warn when exposing a name fails.
        """
        for name in names:
            try:
                cls._expose(name)
            except Exception:
                warnings.warn(
                    "problem creating %s.%s\n%s"
                    % (cls.__name__, name, traceback.format_exc()),
                    RuntimeWarning)


@utils.register(abcoll.MutableSequence)
class CallbackList(_CallbackBase):
    """A list that runs callbacks when its content changes.

    >>> def callback(old, new):
    ...     print("before cl contained", old, "and now it contains", new)
    ...
    >>> cl = CallbackList([1])
    >>> cl
    CallbackList([1])
    >>> cl[:]       # slicing and methods return regular lists
    [1]
    >>> cl._callbacks.append(callback)
    >>> cl.extend([2, 3, 4])
    before cl contained [1] and now it contains [1, 2, 3, 4]
    >>> cl[2:]      # again, a regular list
    [3, 4]
    >>> del cl[:]
    before cl contained [1, 2, 3, 4] and now it contains []
    >>> del cl[:]     # it was already empty, no need to run callbacks
    >>> cl
    CallbackList([])
    """

    __slots__ = ()  # Prevent attaching other attributes.
    _basetype = list


# The __eq__, __ne__, __gt__, __ge__, __lt__ and __le__ will make two
# CallbackLists compare each other's _data. For example, this is what
# __eq__ will do:
#
#                        a == b
#                           |
#                           |
#                      a.__eq__(b)
#                           |
#                           |
#                      a._data == b
#                    /              \
#                   /                \
#          a._data.__eq__(b)   b.__eq__(a._data)
#                 |                    |
#                 |          ,--------------------.
#           NotImplemented   | b._data == a._data |
#                            `--------------------'
CallbackList._expose_all(set(dir(list)) - set(dir(object)))


@utils.register(abcoll.MutableMapping)
class CallbackDict(_CallbackBase):
    """A dictionary that runs callbacks when its content changes.

    >>> def callback(old, new):
    ...     print("before d contained", old, "and now it contains", new)
    ...
    >>> d = CallbackDict(a=1)
    >>> d
    CallbackDict({'a': 1})
    >>> d.copy()    # return a regular dictionary
    {'a': 1}
    >>> d._callbacks.append(callback)
    >>> del d['a']
    before d contained {'a': 1} and now it contains {}
    >>> d.update({'b': 2})
    before d contained {} and now it contains {'b': 2}
    >>> d['b'] = 2      # it was already 2, no need to run callbacks
    >>> d.clear()
    before d contained {'b': 2} and now it contains {}
    """

    __slots__ = ()
    _basetype = dict

    # We can't expose this like other methods because it's a
    # classmethod.
    @classmethod
    def fromkeys(cls, iterable, value=None):
        """Create a new CallbackDict from an iterable of keys.

        >>> CallbackDict.fromkeys(['hello'])
        CallbackDict({'hello': None})
        >>> CallbackDict.fromkeys(['hello'], 'there')
        CallbackDict({'hello': 'there'})
        """
        return cls(dict.fromkeys(iterable, value))


CallbackDict._expose_all(set(dir(dict)) - set(dir(object)) - {'fromkeys'})


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
