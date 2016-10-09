from bananagui import Property, _base
from .bases import Child


try:
    _SpinnerBase = _base._SpinnerBase
except AttributeError:
    # The base doesn't provide a spinner. We need to create one using
    # other widgets.
    from bananagui.bases.defaults import Spinner as _SpinnerBase


class Spinner(_SpinnerBase, Child):

    spinning = Property(
        'spinning', type=bool, default=False,
        doc="True if the widget is currently spinning, False if not.")
