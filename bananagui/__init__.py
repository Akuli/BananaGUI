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
    'HORIZONTAL', 'VERTICAL', 'LEFT', 'CENTER', 'RIGHT', 'RUN_AGAIN',
    'load',
]


# These constants can be used with these variables or with their values
# directly.
HORIZONTAL = 'h'
VERTICAL = 'v'

LEFT = 'l'
CENTER = 'c'
RIGHT = 'r'

# This is not 0 or 1 because returning True or False from a callback
# must not be allowed.
RUN_AGAIN = -1


_wrapper = None


def load(*args, init_mainloop=True):
    """Load a BananaGUI wrapper module.

    The arguments should be Python module names. If they are relative,
    they will be treated as relative to bananagui.wrappers. For example,
    '.tkinter' is equivalent to 'bananagui.wrappers.tkinter'.

    If multiple wrapper modules are given, attempt to load each one until
    loading one of them succeeds. You can import bananagui.gui after
    calling this.

    For convenience, bananagui.mainloop.init() will be called if
    init_mainloop is True.
    """
    assert args, "specify at least one module"

    global _wrapper
    if _wrapper is not None:
        raise RuntimeError("don't call bananagui.load() twice")

    if len(args) == 1:
        # Make sure the wrapper can be imported and THEN set _wrapper to it.
        fullname = utils.resolve_modulename(args[0], 'bananagui.wrappers')
        utils.import_module(fullname)
        _wrapper = fullname    # mainloop.init() needs this.
        if init_mainloop:
            mainloop.init()
    else:
        # Attempt to load each wrapper.
        for arg in args:
            try:
                load(arg)
                return
            # I have no idea what different toolkits can raise.
            except Exception:
                pass
        raise ImportError("cannot load any of the requested wrapper modules")


# This is a bit hacky because different things can come from the wrapper
# or an alternative default wrapper.
@functools.lru_cache()
def _get_wrapper(name):
    """Get an object from the wrapper module.

    For example, if bananagui.load has been called with '.tkinter',
    _get_wrapper('a.b:c') imports bananagui.wrappers.tkinter.a.b and
    returns its c attribute. An exception is raised if load() hasn't
    been called.
    """
    if _wrapper is None:
        raise RuntimeError("bananagui.load() wasn't called")

    modulename, attribute = name.split(':')
    try:
        wrappermodule = utils.import_module(_wrapper + '.' + modulename)
        return getattr(wrappermodule, attribute)
    except (ImportError, AttributeError):
        # Use a default, if any.
        pass

    try:
        defaultmodule = utils.import_module(
            'bananagui.wrappers.defaults.' + modulename)
        return getattr(defaultmodule, attribute)
    except (ImportError, AttributeError):
        # We don't have a default :(
        pass

    raise NotImplementedError("cannot find a wrapper for %s" % name)
