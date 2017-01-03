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

# flake8: noqa

"""BananaGUI tests.

This file sets up a BananaGUI wrapper. If you use the -m option to run
the tests, this file will always be ran also.
"""

import sys
try:
    import faulthandler
    faulthandler.enable()
except ImportError:
    # Python 3.2.
    pass

import bananagui

# We need to ignore everything except the last argument because there
# are coverage's arguments in sys.argv when this is running under
# coverage.
if len(sys.argv) < 2:
    print("Usage: yourpython -m guitests LOAD_ARG", file=sys.stderr)
    sys.exit(1)
bananagui.load(sys.argv[-1])
