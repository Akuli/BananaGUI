"""Wrapper module for other GUI toolkits.

With BananaGUI you can write a GUI application in Python, and then run
the same code using GTK+ 3 or Tkinter. BananaGUI may feature Qt support
later.
"""

import threading
import types
import warnings

# most submodules import this, so it needs to be here
# this contains the real GUI toolkit's modules, see _load_toolkit()
_modules = types.SimpleNamespace()

from bananagui._mainloop import init as _init_mainloop
from bananagui._mainloop import run, quit, add_timeout, RUN_AGAIN
from bananagui._types import UpdatingObject, UpdatingProperty, Callback
from bananagui._widgets.base import Orient, Align, Widget, ChildWidget
from bananagui._widgets.labels import Label
#from bananagui._widgets.buttons import Button
from bananagui._widgets.parents import Parent, Bin
from bananagui._widgets.window import Window, Dialog


__author__ = 'Akuli'
__copyright__ = 'Copyright (c) 2016-2017 Akuli'
__license__ = 'MIT'
__version__ = '0.1-dev'


def _load_dummy():
    return {}


def _load_tkinter():
    import tkinter
    from tkinter import colorchooser, font, messagebox
    from bananagui import _tk_tooltip
    return {'tk': tkinter, 'colorchooser': colorchooser, 'font': font,
            'messagebox': messagebox, 'tk_tooltip': _tk_tooltip}


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


_toolkits = {
    'dummy': _load_dummy, 'tkinter': _load_tkinter,
    'gtk2': (lambda: _load_gtk(2)), 'gtk3': (lambda: _load_gtk(3))}


def _load_toolkit(name):
    # Make sure that all required modules can be imported and THEN set
    # them to _modules.
    if name not in _toolkits:
        raise ValueError("invalid toolkit name %r" % name)

    attributes = _toolkits[name]()
    _modules.name = name
    for attr, value in attributes.items():
        setattr(_modules, attr, value)


def init(toolkit_name):
    """Tell BananaGUI to use the given GUI toolkit and set up everything.

    Currently valid toolkit names are ``'tkinter'``, ``'gtk2'`` and
    ``'gtk3'``. The *toolkit_name* can also be a list or some other
    iterable of toolkit names. For example, ``init(['gtk3', 'tkinter'])``
    attempts to load GTK 3, but tkinter is used instead if it isn't
    installed.

    This function must be called before using most things in BananaGUI.
    For example, all widgets need this.
    """
    if threading.current_thread() is not threading.main_thread():
        raise RuntimeError(
            "bananagui.init() must be called from the main thread")
    if hasattr(_modules, 'name'):
        raise RuntimeError("don't call bananagui.init() twice")

    if isinstance(toolkit_name, str):
        _load_toolkit(toolkit_name)
    else:
        for name in toolkit_name:
            try:
                _load_toolkit(name)
                break
            except Exception:
                # I have no idea what different toolkits can raise.
                # TODO: log the error or somehow show it with the final
                # ImportError raised below, maybe with __cause__ stuff?
                pass
        else:
            # no breaks, nothing succeeded
            raise ImportError("cannot load any of the requested GUI toolkits")

    _init_mainloop()
