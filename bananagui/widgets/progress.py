from bananagui import _get_wrapper, types
from .basewidgets import Child


@types.add_property(
    'progress', type=(float, int), minimum=0, maximum=1,
    doc="""The progressbar's position.

    This is always between 0 and 1.
    """)
class Progressbar(Child):
    """A progress bar widget.

    .. code-block:: none

       ,-------------------.
       | OOOOOOOOOOO       |
       `-------------------'

    The progress bar is always horizontal. Contact me if you need a
    vertical progress bar and I'll implement it.
    """

    def __init__(self, *, progress=0, **kwargs):
        """Initialize the progress bar."""
        self._prop_progress = 0
        wrapperclass = _get_wrapper('widgets.progress:Progressbar')
        self._wrapper = wrapperclass(self)
        super().__init__(**kwargs)
        self.progress = progress

    def _repr_parts(self):
        return ['progress=' + repr(self.progress)] + super()._repr_parts()


@types.add_property('bouncing', type=bool,
                    doc="True if the widget actually bounces.")
class BouncingProgressbar(Child):
    """A progressbar-like widget that bounces back and forth.

    .. code-block:: none

       ,-------------------.
       |           OOOO    |
       `-------------------'

    The progressbar doesn't bounce by default. Set :attr:`~bouncing` to
    True to make it bounce.
    """

    def __init__(self, *, bouncing=False, **kwargs):
        """Initialize the widget."""
        self._prop_bouncing = False
        wrapperclass = _get_wrapper('widgets.progress:BouncingProgressbar')
        self._wrapper = wrapperclass(self)
        super().__init__(**kwargs)
        self.bouncing = bouncing

    def _repr_parts(self):
        return ['bouncing=' + repr(self.bouncing)] + super()._repr_parts()
