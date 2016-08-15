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

"""Handy utilities."""


class _IntEnumMeta(type):
    """A metaclass for IntEnum."""

    def __new__(metaclass, name, bases, dictionary):
        """Create a new IntEnum class."""
        cls = super().__new__(metaclass, name, bases, dictionary)
        for name, value in dictionary.items():
            if not name.startswith('__'):
                setattr(cls, name, cls(value, new_value_name=name))
        return cls

    def __call__(cls, value, *, new_value_name=None):
        """Return an enum from the class dictionary.

        If new_value_name is not None, add a new value to the dictionary
        with the given name when an existing value is not available.
        """
        for enum in cls:
            if enum == value:
                return enum
        if new_value_name is None:
            raise LookupError("{!r} is not a valid {}"
                              .format(integer, cls.__name__))
        value = super().__call__(value)
        value.name = new_value_name
        setattr(cls, new_value_name, value)
        return value

    def __repr__(cls):
        """A repr() for the enum class."""
        return '<enum {}>'.format(cls.__name__)

    __str__ = __repr__

    def __iter__(cls):
        """Yield the created enums."""
        return (enum for enum in cls.__dict__.values()
                if isinstance(enum, cls))


class Enum(metaclass=_IntEnumMeta):
    """Much like Enum in the enum module."""

    def __repr__(self):
        """Return a representation of the enum."""
        return '<enum {}.{}: {}>'.format(
            type(self).__name__,
            self.name,
            super().__repr__(),
        )

    __str__ = __repr__


# Use the real Enum if possible.
try:
    from enum import Enum   # noqa
except ImportError:
    pass


class IntEnum(int, Enum):
    """An integer enumeration."""


class ColorEnum(str, Enum):
    """A color enumeration."""


# Override the IntEnum with a real IntEnum if possible.


class BananaPhone(IntEnum):
    """Ring ring ring ring ring ring ring! Banana Phone."""

    banana = 1
    phone = 2
    bananaphone = banana | phone


print(type(BananaPhone.banana))
print(BananaPhone.banana)
print(BananaPhone.phone)
print(BananaPhone.bananaphone)

print(BananaPhone(1))
print(BananaPhone(2))
print(BananaPhone(3))
