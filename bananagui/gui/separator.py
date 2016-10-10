from bananagui import _base, HORIZONTAL, VERTICAL
from .bases import _Oriented, Child


class Separator(_Oriented, _base.Separator, Child):

    def __init__(self, parent, orientation, **kwargs):
        # Make the separator expand by default.
        if orientation == HORIZONTAL:
            kwargs.setdefault('expand', (True, False))
        if orientation == VERTICAL:
            kwargs.setdefault('expand', (False, True))
        super().__init__(parent, orientation, **kwargs)
