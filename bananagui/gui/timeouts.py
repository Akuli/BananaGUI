"""Timeout class."""

from bananagui import _base
from bananagui.structures import Callback


# Don't allow returning True to run again.
RUN_AGAIN = 2

# This is the only way to make sure that the base gets access to this
# constant I can think of. Another alternative would be to use a class,
# but I think it would be overkill for this.
_base.add_timeout.RUN_AGAIN = RUN_AGAIN


def add_timeout(milliseconds: int, function, *args, **kwargs):
    """Run callback(*args, **kwargs) after waiting.

    If the callback returns RUN_AGAIN it will be called again after
    waiting again. Depending on the GUI toolkit, the timing may start
    when bananagui.main() is started or before it.

    The waiting time is not guaranteed to be exact, but it's good enough
    for most purposes. Use something like time.time() if you need to
    measure time in the callback function.
    """
    assert milliseconds > 0, "non-positive timeout %r" % (milliseconds,)
    _base.add_timeout(milliseconds, Callback(callback, *args, **kwargs))
