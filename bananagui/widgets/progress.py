# Copyright (c) 2016 Akuli

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

"""Widgets that indicate progress."""

import bananagui
from bananagui import types
from .basewidgets import Child


@types.add_property('progress')
class Progressbar(Child):
    """A progress bar widget.

        ,-------------------.
        | OOOOOOOOOOO       |
        `-------------------'

    The progress bar is always horizontal. Contact me if you need a
    vertical progress bar and I'll implement it.

    Attributes:
      progress      The progressbar's position.
                    This is always between 0 and 1 (inclusive).
    """

    def __init__(self, parent, *, progress=0, **kwargs):
        self._progress = 0
        baseclass = bananagui._get_base('widgets.progress:Progressbar')
        self._base = baseclass(self, parent._base)
        super().__init__(parent, **kwargs)
        self.progress = progress

    def _repr_parts(self):
        return ['progress=' + repr(self.progress)] + super()._repr_parts()

    def _check_progress(self, progress):
        # This also checks the type because we can't compare with a
        # value of a wrong type.
        assert 0 <= progress <= 1


@types.add_property('bouncing')
class BouncingProgressbar(Child):
    """A Progressbar-like widget that bounces back and forth.

        ,-------------------.
        |           OOOO    |
        `-------------------'

    This doesn't bounce by default. Set bouncing to True to make it
    bounce.

    Attributes:
      bouncing      True if the widget bounces back and forth.
    """

    def __init__(self, parent, *, bouncing=False, **kwargs):
        self._bouncing = False
        baseclass = bananagui._get_base('widgets.progress:BouncingProgressbar')
        self._base = baseclass(self, parent._base)
        super().__init__(parent, **kwargs)
        self.bouncing = bouncing

    def _repr_parts(self):
        return ['bouncing=' + repr(self.bouncing)] + super()._repr_parts()

    def _check_bouncing(self, bouncing):
        assert isinstance(bouncing, bool)


@types.add_property('spinning')
class Spinner(Child):
    r"""A waiting spinner.

          .---.
         /     \
        | .   O |
         \ - o /
          `---'

    The spinner doesn't spin by default. You can set spinning to True
    to make it spin.

    Attributes:
      spinning      True if the widget is currently spinning, False if not.
    """

    def __init__(self, parent, *, spinning=False, **kwargs):
        self._spinning = False
        baseclass = bananagui._get_base('widgets.progress:Spinner')
        self._base = baseclass(self, parent._base)
        super().__init__(parent, **kwargs)
        self.spinning = spinning

    def _repr_parts(self):
        return ['spinning=' + repr(self.spinning)] + super()._repr_parts()

    def _check_spinning(self, spinning):
        assert isinstance(spinning, bool)
