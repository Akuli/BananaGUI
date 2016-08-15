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

"""Static-ish typing for Python using descriptors.

The descriptors in this module convert their values automatically. For
example:

    >>> class Foo:
    ...     bar = Integer()
    ...
    >>> foo = Foo()
    >>> foo.bar = 10
    >>> foo.bar
    10
    >>> foo.bar = 21.7
    >>> foo.bar
    21
    >>> foo.bar = 'hello'
    Traceback (most recent call last):
      ...
    ValueError: invalid literal for int() with base 10: 'hello'
    >>>

Inspired by David Beazley's metaprogramming presentation.
<http://www.dabeaz.com/py3meta/Py3Meta.pdf>
"""

# Allow using a default value and None as a non-default.
_NOTHING = object()


class DescriptorBase:
    """A basic descriptor."""

    def __init__(self, default=_NOTHING):
        self.default = default
        # Keys are id's of the instances, and values are the
        # descriptors. Using id's does not add an extra reference to the
        # instance.
        self.__values = {}

    def __set__(self, instance, value):
        self.__values[id(instance)] = value

    def __get__(self, instance, cls):
        try:
            return self.__values[id(instance)]
        except KeyError as e:
            if self.default is _NOTHING:
                raise ValueError("the value has not been set") from e
            return self.default

    def convert(self, value):
        """Override this in a subclass."""
        return value


class IsInstance(DescriptorBase):
    """A descriptor that uses isinstance() for checking the values.

    Inherit from this, and set a required_type class attribute.
    """

    def __set__(self, instance, value):
        required_type = type(self).required_type
        if not isinstance(value, required_type):
            raise TypeError("expected %s, got %r"
                            % (required_type.__name__, value))
        super().__set__(instance, value)

    @classmethod
    def from_type(cls, required_type, *, or_none=False):
        """Create a new IsInstance subclass from a required type.

        If or_none is True, also inherit from OrNone.
        """
        return type(
            required_type.__name__ + 'Descriptor',
            (OrNone, cls) if or_none else (cls,),
            {'required_type': required_type},
        )


class Integer(DescriptorBase):
    """An integer.

    By default, this converts the values with int(value), but you can
    specify another base on initialization with the base keyword
    argument.
    """

    def __init__(self, base=None, **kwargs):
        super().__init__(**kwargs)
        self.base = base

    def __set__(self, instance, value):
        if self.base is None:
            value = int(value)
        else:
            value = int(value, self.base)
        super().__set__(instance, value)


class NonNegative(DescriptorBase):
    """A non-negative value."""

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("%r is negative" % (value,))
        super().__set__(instance, value)


class Boolean(DescriptorBase):
    """A Boolean value."""

    def __set__(self, instance, value):
        super().__set__(instance, bool(value))


class String(DescriptorBase):
    """A descriptor that converts to string."""

    def __set__(self, instance, value):
        super().__set__(instance, str(value))


class Sized(DescriptorBase):
    """A descriptor that checks the length."""

    def __init__(self, length, **kwargs):
        super().__init__(**kwargs)
        self.length = length

    def __set__(self, instance, value):
        if len(value) != self.length:
            raise ValueError("the length of %r is not %d"
                             % (value, self.length))
        super().__set__(instance, value)


class Tuple(Sized):
    """A descriptor that converts to tuple.

    Optional length and types keyword arguments can be given on
    initialization. Length is the length of the tuple, and types should
    be a tuple of other descriptor classes the tuple should contain.
    """

    def __init__(self, types=None, length=None, **kwargs):
        if length is None and types is not None:
            # Get the length from types.
            types = tuple(types)
            length = len(types)
        elif types is None and length is not None:
            # Get the types from the length.
            length = int(length)
            types = (object,) * length
        else:
            raise ValueError("specify length or types, but not both")
        super().__init__(length=length, **kwargs)
        self.types = types

    def __set__(self, instance, value):
        value = tuple(value)
        for required_type, item in zip(self.types, value):
            if not isinstance(item, required_type):
                raise TypeError("expected %s, got %r"
                                % (required_type.__name__, item))
        super().__set__(instance, value)


class OrNone(DescriptorBase):
    """A descriptor that also allows None as the value.

    This works by calling super() in __set__ only if the value is not
    None, and setting it directly to the values if it is None.
    """

    def __set__(self, instance, value):
        if value is None:
            # Bypass the checks.
            # This may get called twice, but it doesn't matter.
            DescriptorBase.__set__(self, instance, value)
        else:
            super().__set__(instance, value)


class Whitelisted(DescriptorBase):
    """A value in a whitelist.

    The whitelist is specified on initialization, and it can be any
    object that allows checking if it contains another object.
    """

    def __init__(self, whitelist, **kwargs):
        super().__init__(**kwargs)
        self.whitelist = whitelist

    def __set__(self, instance, value):
        if value not in self.whitelist:
            raise ValueError("%r is not in the whitelist" % (value,))
        super().__set__(instance, value)


# Mixin classes.
# The order of baseclasses is important.

class NonNegativeInteger(Integer, NonNegative):
    """A non-negative integer."""


class WhitelistedInteger(Integer, Whitelisted):
    """A whitelisted integer."""


class NonNegativeIntegerOrNone(OrNone, NonNegativeInteger):
    """A non-negative integer or None."""


class StringOrNone(OrNone, String):
    """A string or None."""
