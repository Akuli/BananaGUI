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

"""Simple wrapper for GUI frameworks."""

import importlib


class MissingFeatureWarning(UserWarning):
    """Warned when a GUI toolkit doesn't have the requested feature."""


def get(*toolkit_names):
    """Attempt to return a toolkit from toolkit_names.

    The first one is returned, and if it's not avaliable the next one is
    etc.
    """
    if not toolkit_names:
        raise ValueError("no toolkit names were specified")
    for name in toolkit_names:
        try:
            return importlib.import_module('bananagui.wrappers.' + name)
        except ImportError:
            pass
    raise ImportError("cannot import any of the required toolkits")
