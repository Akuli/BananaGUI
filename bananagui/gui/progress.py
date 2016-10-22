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

import bananagui
from bananagui import _base, utils
from bananagui.bases import defaults
from .basewidgets import Child, Oriented


class Progressbar(Oriented, _base.Progressbar, Child):
    """A progress bar widget."""

    progress = bananagui.BananaProperty(
        'progress', type=(float, int), minimum=0, maximum=1, default=0,
        doc="The progressbar's position.")


class BouncingProgressbar(Oriented, _base.BouncingProgressbar, Child):
    """A Progressbar-like widget that bounces back and forth.

    This doesn't bounce by default. Set the bouncing property to True to
    make it bounce.
    """

    bouncing = bananagui.BananaProperty(
        'bouncing', type=bool, default=False,
        doc="True if the progress bar is bouncing, False if not.")


class Spinner(utils.find_attribute('Spinner', _base, defaults), Child):
    """A waiting spinner.

    The spinner doesn't spin by default. You can set the spinning
    property to True to make it spin.
    """

    spinning = bananagui.BananaProperty(
        'spinning', type=bool, default=False,
        doc="True if the widget is currently spinning, False if not.")
