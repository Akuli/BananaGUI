"""Value and type assertion functions."""


def check(value, *, allow_none=False, required_type=None, length=None,
          minimum=None, maximum=None):
    if value is None:
        assert allow_none, "the value must not be None"
        return
    if required_type is not None:
        assert isinstance(value, required_type), \
            ("expected an instance of %s, got %r"
             % (required_type.__name__, value))
    if length is not None:
        assert len(value) == length, \
            "expected a value of length %d, got %r" % (length, value)
    if minimum is not None:
        assert value >= minimum, "%r is smaller than %r" % (value, minimum)
    if maximum is not None:
        assert value <= maximum, "%r is larger than %r" % (value, maximum)


def pair(pair, **check_kwargs):
    """Check a pair."""
    assert isinstance(pair, tuple), "expected a tuple, got %r" % (pair,)
    assert len(pair) == 2, "length of %r is not 2" % (pair,)
    first, second = pair
    check(first, **check_kwargs)
    check(second, **check_kwargs)


def deprecated(f):
    def doit(*a,**k):
        __import__('warnings').warn('%s is deprecated'%f.__name__,DeprecationWarning)
        return f(*a,**k)
    return doit

intpair = deprecated(functools.partial(pair, required_type=int))
positive_intpair = deprecated(functools.partial(intpair, minimum=1)
boolpair = deprecated(functools.partial(pair, required_type=bool))
