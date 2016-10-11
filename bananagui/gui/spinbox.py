from bananagui import Property
from .bases import Child


class Spinbox(_base.Spinbox, Child):

    minimum = Property(
        'start', type=(int, float), default=0,
        doc="The smallest value the spinbox can have.")
    maximum = Property(
        'stop', type=(int, float), default=100,
        doc="The largest value the spinbox can have.")
    step = Property(
        'step', type=(int, float), default=1, minimum=0,
        doc="The increment size.")

    def _bananagui_set_minimum(self, value):
        assert value <= self['maximum'], "start is bigger than stop"
        super()._bananagui_set_minimum(value)

    def _bananagui_set_maximum(self, value):
        assert value >= self['minimum'], "stop is bigger than start"
        super()._bananagui_set_stop(stop)

    def _bananagui_set_step(self, step):
        assert step < self['stop'] - self['start'], "too big step"
