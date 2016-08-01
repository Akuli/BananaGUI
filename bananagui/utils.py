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

import sys


class _EnumInt(int):

    def __str__(self):
        return '{}.{}'.format(self.classname, self.name)

    def __repr__(self):
        return '<{}: {}>'.format(str(self), int(self))


class _IntEnumMeta(type):

    def __new__(cls, name, bases, dictionary):
        for key, value in dictionary.items():
            if not key.startswith('_'):
                enum = _EnumInt(value)
                enum.classname = name
                enum.name = key
                dictionary[key] = enum
        return type.__new__(cls, name, bases, dictionary)

    def __iter__(cls):
        values = [value for key, value in cls.__dict__.items()
                  if not key.startswith('_')]
        values.sort(key=int)
        # Python 3.2 doesn't do yield from.
        for value in values:
            yield value

    def __call__(cls, value):
        """Look up an enum by its integer value."""
        for enum in cls.__dict__.values():
            if enum == value:
                return enum
        raise ValueError('{} is not a valid {}'.format(value, cls.__name__))


class IntEnum(metaclass=_IntEnumMeta):
    """An IntEnum class for Python 3.2 and 3.3.

    The enum module was added in Python 3.4.
    """


class BananaPhone(IntEnum):
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
