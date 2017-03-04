"""Handy dialog functions.

All public functions in this module take these arguments:

- *parentwindow:* A :class:`bananagui.widgets.Window` object. Usually
  the dialog will be centered on this window.
- *title:* The title of the dialog, defaults to *parentwindow*'s
  title.

The :func:`~info`, :func:`~warning`, :func:`~error` and
:func:`~question` functions also take these arguments:

- *buttons:* This should be an iterable of button texts that will be
  added to the dialog. BananaGUI may need to iterate over this multiple
  times, so I don't recommend using an iterator for this.
- *defaultbutton:* This should be a string in *buttons*. The default
  button will have keyboard focus by default.
- *text:* This is the text that will be shown in the dialog.
- *title:* The title of the dialog, defaults to the parentwindow's title.

The functions return whatever the user chooses or None if the dialog is
closed. For example, :func:`info`, :func:`warning`, :func:`error` and
:func:`question` return the text of the clicked button or None.
"""

from bananagui import _get_wrapper, color

__all__ = ['info', 'warning', 'error', 'question', 'colordialog']


def _message(icon, parentwindow, msg, title, buttons, defaultbutton):
    if title is None:
        title = parentwindow.title
    if defaultbutton is not None and defaultbutton not in buttons:
        raise ValueError("default button %r not in buttons"
                         % (defaultbutton,))
    # The wrapper functions can't import the MessageKind enum from this
    # module, so they get the name of tne enum member instead.
    wrapperfunc = _get_wrapper('msgbox:message')
    return wrapperfunc(icon, parentwindow, msg, title, buttons,
                       defaultbutton)


def info(parentwindow, message, buttons, *,
         title=None, defaultbutton=None):
    """Display an information message."""
    return _message('info', parentwindow, message, title, buttons,
                    defaultbutton)


def warning(parentwindow, message, buttons, *,
            title=None, defaultbutton=None):
    """Display a warning message."""
    return _message('warning', parentwindow, message, title, buttons,
                    defaultbutton)


def error(parentwindow, message, buttons, *,
          title=None, defaultbutton=None):
    """Display an error message."""
    return _message('error', parentwindow, message, title, buttons,
                    defaultbutton)


def question(parentwindow, message, buttons, *,
             title=None, defaultbutton=None):
    """Display a question message."""
    return _message('question', parentwindow, message, title, buttons,
                    defaultbutton)


def colordialog(parentwindow, *, title=None, defaultcolor=color.BLACK):
    """Ask a color from the user.

    This returns the new color, or None if the user canceled the dialog.
    """
    if title is None:
        title = parentwindow.title
    if not color._is_valid_color(defaultcolor):
        raise ValueError(
            "%r is not a valid '#RRGGBB' color, use "
            "bananagui.color to convert it" % (defaultcolor,))
    wrapperfunc = _get_wrapper('msgbox:colordialog')
    return wrapperfunc(parentwindow, defaultcolor, title)


# def fontdialog(parentwindow, *, title=None, defaultfont=bananagui.Font()):
#    """Ask a font from the user.
#
#    This returns the new font, or None if the user canceled the dialog.
#    """
#    if title is None:
#        title = parentwindow.title
#    return _wrapper.fontdialog(parentwindow, defaultfont, title)
