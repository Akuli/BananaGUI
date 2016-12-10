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

"""Wrapper module for other GUI toolkits.

With BananaGUI you can write a GUI application in Python, and then run
the same code using any of the supported GUI toolkits, including PyQt5,
GTK+ 3 and tkinter.
"""

import functools

from bananagui import mainloop, utils


__author__ = 'Akuli'
__copyright__ = 'Copyright (c) 2016 Akuli'
__license__ = 'MIT'
__version__ = '0.1-dev'
__all__ = [
    # Submodules.
    'color', 'font', 'iniloader', 'mainloop', 'msgbox', 'widgets',

    # Things defined here.
    'HORIZONTAL', 'VERTICAL', 'RUN_AGAIN', 'load',
]


# These constants can be used with these variables or with their values
# directly.
HORIZONTAL = 'h'
VERTICAL = 'v'

# This is not 0 or 1 because returning True or False from a callback
# must not be allowed.
RUN_AGAIN = -1


_base = None


def load(*args, init_mainloop=True):
    """Load a BananaGUI base module.

    The arguments should be Python module names. If they are relative,
    they will be treated as relative to bananagui.bases. For example,
    '.tkinter' is equivalent to 'bananagui.bases.tkinter'.

    If multiple base modules are given, attempt to load each one until
    loading one of them succeeds. You can import bananagui.gui after
    calling this.

    For convenience, bananagui.mainloop.init() will be called if
    init_mainloop is True. The possibly relative name of the loaded
    base module is returned.
    """
    assert args, "specify at least one module"

    global _base
    if _base is not None:
        raise RuntimeError("don't call bananagui.load() twice")

    if len(args) == 1:
        # Make sure the base can be imported and THEN set _base to it.
        fullname = utils.resolve_modulename(args[0], 'bananagui.bases')
        assert fullname != 'bananagui.bases.defaults', \
            "the '.defaults' base can't be loaded directly"
        utils.import_module(fullname)
        _base = fullname
        if init_mainloop:
            mainloop.init()
        return args[0]
    else:
        # Attempt to load each base.
        for arg in args:
            try:
                return load(arg)
            except ImportError:
                pass
        raise ImportError("cannot load any of the requested base modules")


# This is a bit hacky because different things can come from the base
# or an alternative default base.
@functools.lru_cache()
def _get_base(name):
    """Get an object from the base module.

    For example, if bananagui.load has been called with '.tkinter',
    _get_base('a.b:c') imports bananagui.bases.tkinter.a.b and returns
    its c attribute. An exception is raised if load() hasn't been
    called.
    """
    if _base is None:
        raise ImportError("bananagui.load() wasn't called")

    modulename, attribute = name.split(':')
    basemodule = utils.import_module(_base + '.' + modulename)
    try:
        defaultmodule = utils.import_module(
            'bananagui.bases.defaults.' + modulename)
    except ImportError:
        # There isn't a default base, basemodule needs to have the
        # attribute.
        return getattr(basemodule, attribute)
    # There is a default base, we can use that if the base module
    # doesn't have the attribute.
    try:
        return getattr(basemodule, attribute)
    except AttributeError:
        return getattr(defaultmodule, attribute)
