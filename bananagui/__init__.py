"""Wrapper module for other GUI toolkits.

With BananaGUI you can write a GUI application in Python, and then run
the same code using GTK+ 3 or Tkinter. BananaGUI may feature Qt support
later.
"""

import functools
import types
import warnings

# most submodules import this, so it needs to be here
# this contains the real GUI toolkit's modules
_modules = types.SimpleNamespace()

from bananagui import mainloop
from bananagui._constants import Orient, Align, RUN_AGAIN
from bananagui._types import Callback
from bananagui._widgets.base import UpdatingProperty, Widget, ChildWidget
from bananagui._widgets.labels import Label
from bananagui._widgets.window import Window


__author__ = 'Akuli'
__copyright__ = 'Copyright (c) 2016-2017 Akuli'
__license__ = 'MIT'
__version__ = '0.1-dev'


def _load_dummy():
    return {}


def _load_gtk(version):
    import gi

    if version == 2:
        # gi is meant to be used with gtk 3, so it warns about using it
        # with gtk 2
        warnings.filterwarnings(
            'ignore', r'^You have imported the Gtk 2\.0 module\.')

    gi.require_version('Gtk', '%d.0' % version)
    gi.require_version('Gdk', '%d.0' % version)
    gi.require_version('GLib', '2.0')

    from gi.repository import Gtk, Gdk, GLib
    return {'Gtk': Gtk, 'Gdk': Gdk, 'GLib': GLib}


def _load_tkinter():
    import tkinter
    from tkinter import colorchooser, font, messagebox
    return {'tk': tkinter, 'colorchooser': colorchooser,
            'font': font, 'messagebox': messagebox}


_toolkits = {'dummy': _load_dummy, 'tkinter': _load_tkinter,
             'gtk2': functools.partial(_load_gtk, 2),
             'gtk3': functools.partial(_load_gtk, 3)}


def _load_toolkit(name):
    # Make sure that all required modules can be imported and THEN set
    # them to _modules.
    kwargs = _toolkits[name]()

    _modules.name = name
    for attr, value in kwargs.items():
        setattr(_modules, attr, value)


def load(*toolkits, init_mainloop=True):
    """Tell BananaGUI to use the specified GUI toolkit.

    This function must be called before using most things in BananaGUI.
    Most notably, all widgets need this.

    The arguments for this function should be valid GUI toolkit names.
    For example, ``load('tkinter')`` tells BananaGUI to use tkinter. The
    :data:`WRAPPERS` variable contains a full list of valid arguments
    for this function.

    If multiple arguments are given, this function attempts to import
    each GUI toolkit until importing one of them succeeds.

    For convenience, :func:`bananagui.mainloop.init` will be called if
    *init_mainloop* is True.
    """
    if hasattr(_modules, 'name'):
        raise RuntimeError("don't call load() twice")
    if not toolkits:
        raise TypeError("no toolkits were specified")

    if len(toolkits) == 1:
        if toolkits[0] not in _toolkits:
            raise ValueError("invalid toolkit name %r" % toolkits)

        _load_toolkit(toolkits[0])
        if init_mainloop:
            mainloop.init()

    else:
        # Attempt to load each toolkit.
        for arg in toolkits:
            if arg not in WRAPPERS:
                raise ValueError("invalid toolkit name %r" % (arg,))

            try:
                _load_toolkit(arg)
            except Exception:
                # I have no idea what different toolkits can raise.
                # TODO: log the error or somehow show it with the final
                # ImportError raised below, maybe with __cause__ stuff?
                continue

            if init_mainloop:
                mainloop.init()
            return

        raise ImportError("cannot load any of the requested GUI toolkits")
