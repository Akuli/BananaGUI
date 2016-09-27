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


def intpair(pair):
    """Make sure that two items of a pair are positive integers."""
    check(pair, required_type=tuple, length=2)
    first, second = pair
    assert isinstance(first, int), "expected an integer, got %r" % (pair,)
    assert isinstance(second, int), "expected an integer, got %r" % (pair,)


def positive_intpair(pair):
    """Make sure that two items of a pair are positive integers."""
    intpair(pair)
    first, second = pair
    assert first > 0, "expected a positive value, got %r" % (first,)
    assert second > 0, "expected a positive value, got %r" % (second,)


def boolpair(pair):
    check(pair, required_type=tuple, length=2)
    first, second = pair
    assert isinstance(first, bool), "%r is not a Boolean" % (first,)
    assert isinstance(second, bool), "%r is not a Boolean" % (second,)
