"""Value and type assertion functions."""

import functools


def check(value, *, pair=False, allow_none=False, required_type=None,
          length=None, minimum=None, maximum=None):
    if pair:
        # Everything is different.
        kwargs = locals().copy()
        del kwargs['value']
        del kwargs['pair']
        assert isinstance(value, tuple), "%r is not a tuple" % (value,)
        assert len(value) == 2, "length of %r is not 2" % (value,)
        first, second = pair
        check(first, **kwargs)
        check(second, **kwargs)
        return

    if value is None:
        assert allow_none, "the value must not be None"
        return
    if required_type is not None:
        assert isinstance(value, required_type), \
            ("expected an instance of %r, got %r"
             % (required_type.__name__, value))
    if length is not None:
        assert len(value) == length, \
            "expected a value of length %d, got %r" % (length, value)
    if minimum is not None:
        assert value >= minimum, "%r is smaller than %r" % (value, minimum)
    if maximum is not None:
        assert value <= maximum, "%r is larger than %r" % (value, maximum)


def deprecated(f):
    def doit(*a,**kw):
        __import__('warnings').warn(f.__name__+' is deprecated',DeprecationWarning)
        return f(*a,**kw)
    return doit


pair = deprecated(functools.partial(check, pair=True))
boolpair = deprecated(functools.partial(pair, required_type=bool))
intpair = deprecated(functools.partial(pair, required_type=int))
positive_intpair = deprecated(functools.partial(intpair, minimum=1))
