"""Print a tree of a widget and its child widgets.

Example::

    >>> window = widgets.Window()
    >>> box = widgets.Box()
    >>> window.add(box)
    >>> for i in range(5):
    ...     box.append(widgets.Label("label %d" % i))
    ...
    >>> widgettree.dump(window)
    bananagui.widgets.Window object, title='BananaGUI Window', contains a child
    └── bananagui.widgets.Box object, contains 5 children
        ├── bananagui.widgets.Label object, text='label 0'
        ├── bananagui.widgets.Label object, text='label 1'
        ├── bananagui.widgets.Label object, text='label 2'
        ├── bananagui.widgets.Label object, text='label 3'
        └── bananagui.widgets.Label object, text='label 4'

If you would like to print a tree of widgets in a BananaGUI ini file,
you can use :mod:`bananagui.iniloader`.
"""

# Unfortunately there isn't a good way to require pytest fixtures from
# doctests, so the docstring isn't tested.

import io
import sys

from bananagui import widgets

__all__ = ['dump', 'dumps']


def _clean_repr(obj, ascii_only):
    if ascii_only:
        result = ascii(obj)
    else:
        result = repr(obj)
    if result.startswith('<') and result.endswith('>'):
        result = result[1:-1]
    return result


def _dump_tree(widget, file, ascii_only, prefix=''):
    children = list(widget.children())
    for index, child in enumerate(children):
        for character in prefix:
            print(character, end=' '*3, file=file)
        childrepr = _clean_repr(child, ascii_only)
        if index == len(children) - 1:
            # This is the last child.
            if ascii_only:
                print('`--', childrepr, file=file)
            else:
                print('└──', childrepr, file=file)
            new_prefix = prefix + ' '
        else:
            # This is not the last child.
            if ascii_only:
                print('|--', childrepr, file=file)
                new_prefix = prefix + '|'
            else:
                print('├──', childrepr, file=file)
                new_prefix = prefix + '│'
        if isinstance(child, widgets.Parent):
            _dump_tree(child, file, ascii_only, new_prefix)


def dump(widget: widgets.Parent, file=None, *, ascii_only=False):
    """Print a tree of a parent widget and its child widgets.

    The *file* defaults to :data:`sys.stdout`. If *ascii_only* is true,
    no non-ASCII characters will be used.
    """
    # This allows monkeypatching sys.stdout.
    if file is None:
        file = sys.stdout
    print(_clean_repr(widget, ascii_only), file=file)
    _dump_tree(widget, file, ascii_only)


def dumps(widget: widgets.Parent, **kwargs):
    """Like :func:`~dump`, but return a string instead of writing to a file."""
    fakefile = io.StringIO()
    dump(widget, fakefile, **kwargs)
    return fakefile.getvalue()
