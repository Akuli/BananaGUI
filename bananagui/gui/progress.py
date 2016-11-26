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

from bananagui import _base, utils
from bananagui.bases import defaults
from .basewidgets import Child


@utils.add_property('progress')
class Progressbar(_base.Progressbar, Child):
    """A progress bar widget.

    Attributes:
      progress      The progressbar's position.
                    This is always between 0 and 1 (inclusive).
    """

    def __init__(self, *args, **kwargs):
        self._progress = 0
        super().__init__(*args, **kwargs)

    def _check_progress(self, progress):
        # This also checks the type because we can't compare with a
        # value of a wrong type.
        assert 0 <= progress <= 1


@utils.add_property('bouncing')
class BouncingProgressbar(_base.BouncingProgressbar, Child):
    """A Progressbar-like widget that bounces back and forth.

    This doesn't bounce by default. Set bouncing to True to make it
    bounce.

    Attributes:
      bouncing      True if the widget bounces back and forth.
    """

    def __init__(self, *args, **kwargs):
        self._bouncing = False
        super().__init__(*args, **kwargs)

    def _check_bouncing(self, bouncing):
        assert isinstance(bouncing, bool)


class Spinner(utils.find_attribute('Spinner', _base, defaults), Child):
    """A waiting spinner.

    The spinner doesn't spin by default. You can set spinning to True
    to make it spin.

    Attributes:
      spinning      True if the widget is currently spinning, False if not.
    """

    def __init__(self, *args, **kwargs):
        self._spinning = False
        super().__init__(*args, **kwargs)

    def _check_spinning(self, spinning):
        assert isinstance(spinning, bool)
