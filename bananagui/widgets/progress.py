# Copyright (c) 2016-2017 Akuli

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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


@types.add_property('spinning', type=bool,
                    doc="True if the widget is currently spinning.")
class Spinner(Child):
    r"""A waiting spinner.

    .. code-block:: none

         .---.
        /     \
       | .   O |
        \ - o /
         `---'

    The spinner doesn't spin by default. Set spinning to True to make
    it spin.
    """

    def __init__(self, *, spinning=False, **kwargs):
        """Initialize the spinner."""
        self._prop_spinning = False
        wrapperclass = _get_wrapper('widgets.progress:Spinner')
        self._wrapper = wrapperclass(self)
        super().__init__(**kwargs)
        self.spinning = spinning

    def _repr_parts(self):
        return ['spinning=' + repr(self.spinning)] + super()._repr_parts()
