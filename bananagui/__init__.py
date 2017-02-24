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

"""Wrapper module for other GUI toolkits.

With BananaGUI you can write a GUI application in Python, and then run 
the same code using GTK+ 3 or Tkinter. BananaGUI may feature Qt support 
later.
"""

import enum
import functools

from bananagui import mainloop, utils


__author__ = 'Akuli'
__copyright__ = 'Copyright (c) 2016-2017 Akuli'
__license__ = 'MIT'
__version__ = '0.1-dev'


class Orient(enum.IntEnum):
    HORIZONTAL = 1
    VERTICAL = 2


class Align(enum.IntEnum):
    LEFT = 1
    CENTER = 2
    RIGHT = 3

    # These are aliases because LEFT and RIGHT are used more often.
    TOP = LEFT
    BOTTOM = RIGHT


# This is not 0 or 1 because returning True or False from a callback
# must not be allowed. I don't think an enum with just one value is
# worth it, so this is just an integer. The callbacks can also return
# None if they are not supposed to run again.

#: If a timeout callback function returns this, it will be called again. 
#: See :func:`bananagui.mainloop.add_timeout` for more info.
RUN_AGAIN = -1

# This needs to be updated when new wrapper modules are added.

#: A set of currently supported wrapper module names.
#:
#: Modifying this is not recommended.
WRAPPERS = {'tkinter', 'gtk3', 'dummy'}

_wrapper = None


def _load_wrapper(name):
    # Make sure the wrapper can be imported and THEN set _wrapper to it.
    global _wrapper
    fullname = 'bananagui.wrappers.' + name
    utils.import_module(fullname)
    _wrapper = fullname


def load_wrapper(*args, init_mainloop=True):
    """Initialize BananaGUI.

    This function must be called before using many things in BananaGUI. 
    See :mod:`bananagui.mainloop` for more information.

    The arguments for this function should be valid BananaGUI wrapper 
    modules. For example, ``load_wrapper('tkinter')`` tells BananaGUI to 
    use tkinter as its GUI toolkit. The :data:`WRAPPERS` variable 
    contains a full list of valid arguments for this function.

    If multiple arguments are given, this function attempts to load each 
    wrapper module until loading one of them succeeds.

    For convenience, :func:`bananagui.mainloop.init` will be called if 
    *init_mainloop* is True.
    """
    if not args:
        raise TypeError("no wrappers were specified")
    if _wrapper is not None:
        raise RuntimeError("don't call load_wrapper() twice")

    if len(args) == 1:
        if args[0] not in WRAPPERS:
            raise ValueError("invalid wrapper name %r" % (arg,))
        _load_wrapper(args[0])
        if init_mainloop:
            mainloop.init()
    else:
        # Attempt to load each wrapper.
        for arg in args:
            if arg not in WRAPPERS:
                raise ValueError("invalid wrapper name %r" % (arg,))
            try:
                _load_wrapper(arg)
            # I have no idea what different toolkits can raise.
            except Exception:
                continue
            if init_mainloop:
                mainloop.init()
            return
        raise ImportError("cannot load any of the requested wrapper modules")


@functools.lru_cache()
def _get_wrapper(name):
    """Get an object from the wrapper module.

    For example, if bananagui.load_wrapper('tkinter') has been ran,
    _get_wrapper('a.b:c') imports bananagui.wrappers.tkinter.a.b and
    returns its c attribute. An exception is raised if
    bananagui.load_wrapper() has not been called.
    """
    if _wrapper is None:
        raise RuntimeError("bananagui.load_wrapper() wasn't called")

    modulename, attribute = name.split(':')
    try:
        wrappermodule = utils.import_module(_wrapper + '.' + modulename)
        return getattr(wrappermodule, attribute)
    except (ImportError, AttributeError):
        # Use a default, if any.
        try:
            defaultmodule = utils.import_module(
                'bananagui.wrappers.defaults.' + modulename)
            return getattr(defaultmodule, attribute)
        except (ImportError, AttributeError) as e:
            # We don't have a default :(
            raise NotImplementedError(
                "cannot find a wrapper for %s" % name) from e
