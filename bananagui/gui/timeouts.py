"""Timeout class."""

from bananagui import _base


# Don't allow returning True to run again.
RUN_AGAIN = 2

# This is the only way to make sure that the base gets access to this
# constant I can think of. Another alternative would be to use a class,
# but I think it would be overkill for this.
_base.add_timeout.RUN_AGAIN = RUN_AGAIN


def add_timeout(milliseconds: int, callback) -> None:
    """Run callback() after waiting.

    If the function returns RUN_AGAIN it will be called again after
    waiting again. Depending on the GUI toolkit, the timing may start
    when bananagui.main() is started or before it.

    The waiting time is not guaranteed to be exact, but it's good enough
    for most purposes. Use something like time.time() if you need to
    measure time in the callback function.
    """
    # TODO: in bases, generate a warning if the function returns
    # something else than None or RUN_AGAIN.
    assert milliseconds > 0, "non-positive timeout %r" % (milliseconds,)
    assert callable(callback), "non-callable callback"
    _base.add_timeout(milliseconds, callback)
