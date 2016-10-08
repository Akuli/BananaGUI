"""BananaGUI's utility functions and other things.

It's not recommended to rely on this submodule. It's meant only for
being used internally by BananaGUI and it can be changed in the future.
"""


def copy_doc(source):
    """Copy __doc__ to another object.

    Unlike functools.wraps, this only copies __doc__ so this also works
    with classes. Use this as a decorator.
    """
    def inner(destination):
        destination.__doc__ = source.__doc__
        return destination

    return inner


def baseclass(cls):
    """Modify cls to prevent creating instances and return it.

    Subclasses of cls can be instantiated normally, and cls may contain
    an __init__ method. Use this as a decorator.
    """
    if 'DEBUG' not in os.environ:
        def new_init(self, *args, **kwargs):
            if type(self) is cls:   # isinstance() can't be used here
                raise TypeError("cannot create instances of %r" % cls.__name__)
            # object.__init__ doesn't take arguments.
            if old_init is not None and old_init is not object.__init__:
                old_init(self, *args, **kwargs)

        # hasattr doesn't work here because we need to check if the
        # __init__ is defined in cls or a baseclass.
        old_init = cls.__dict__.get('__init__', None)
        cls.__init__ = new_init

    return cls


def baseclass(base):
    """Modify a class to prevent creating instances and return it.

    Subclasses of the class can be instantiated normally, and the class
    may define an __init__ method. Use this as a decorator.
    """
    def new_new(cls, *args, **kwargs):
        if cls is base:   # issubclass() can't be used here
            raise TypeError("cannot create instances of %r directly"
                            % cls.__name__)
        if old_new is object.__new__:
            # object.__new__ takes no arguments.
            return old_new(cls)
        return old_new(cls, *args, **kwargs)

    old_new = base.__new__
    base.__new__ = new_new
    return base


def common_beginning(*iterables):
    """Check how many common elements the beginnings of iterables have.

    >>> common_beginning([1, 2, 3, 4], [1, 2, 4, 3])
    2
    >>> common_beginning([2, 1, 3, 4], [1, 2, 3, 4])
    0
    """
    assert len(iterables) >= 2, "two items are needed for comparing"
    result = 0
    rows = iter(zip(*iterables))
    try:
        while len(set(next(rows))) == 1:  # All items of the row are equal.
            result += 1
    except StopIteration:
        pass
    return result


def check(value, *, pair=False, allow_none=False, type=None,
          length=None, minimum=None, maximum=None):
    """Do assertions about the value."""
    if pair:
        # Everything is different.
        assert isinstance(value, tuple), "%r is not a tuple" % (value,)
        assert len(value) == 2, "length of %r is not 2" % (value,)
        kwargs = locals().copy()
        del kwargs['value']
        del kwargs['pair']
        first, second = value
        check(first, **kwargs)
        check(second, **kwargs)
        return

    if not allow_none:
        assert value is not None, "the value must not be None"
    if value is None:
        return
    if type is not None:
        assert isinstance(value, type), \
            "expected an instance of %r, got %r" % (type.__name__, value)
    if length is not None:
        assert len(value) == length, \
            "expected a value of length %d, got %r" % (length, value)
    if minimum is not None:
        assert value >= minimum, "%r is smaller than %r" % (value, minimum)
    if maximum is not None:
        assert value <= maximum, "%r is larger than %r" % (value, maximum)
