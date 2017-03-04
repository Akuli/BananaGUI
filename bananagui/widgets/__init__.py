# flake8: noqa

"""This module contains BananaGUI's widget classes."""


def _fix_modulenames():
    """Make classes and functions seem like they come from here.

    Return an __all__ list.
    """
    result = []
    for name, value in globals().items():
        if callable(value) and not name.startswith('_'):
            value.__module__ = __name__
            result.append(name)
    return result


from .basewidgets import Widget, Child
from .buttons import Button, ImageButton
from .labels import Label, ImageLabel
from .misc import Checkbox, Dummy, Separator
from .parents import Parent, Bin, Box, Scroller, Group
from .progress import Progressbar, BouncingProgressbar
from .ranged import Slider, Spinbox
from .textwidgets import TextBase, Entry, TextEdit
#from .trayicon import TrayIcon
from .window import Window, Dialog

__all__ = _fix_modulenames()
