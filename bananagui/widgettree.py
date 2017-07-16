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
you can use the command-line interface of :mod:`bananagui.iniloader`.
"""

# TODO: update the example and figure out how to test it
# the problem is that it needs the dummywrappper fixture, and there's no
# good way to require it from a doctest

import io
import sys

# __init__.py doesn't import this, no need to import stuff like
# bananagui._widgets here
import bananagui

__all__ = ['dump', 'dumps']


_unicodes = {
    '|--': ('\N{BOX DRAWINGS LIGHT VERTICAL AND RIGHT}'
            '\N{BOX DRAWINGS LIGHT HORIZONTAL}'
            '\N{BOX DRAWINGS LIGHT HORIZONTAL}'),
    '`--': ('\N{BOX DRAWINGS LIGHT ARC UP AND RIGHT}'
            '\N{BOX DRAWINGS LIGHT HORIZONTAL}'
            '\N{BOX DRAWINGS LIGHT HORIZONTAL}'),
    '|': '\N{BOX DRAWINGS LIGHT VERTICAL}',
}


def _dump_tree(widget, file, ascii_only, prefix=''):
    if ascii_only:
        reprfunc = ascii
        unicodify = (lambda string: string)      # noqa
    else:
        reprfunc = repr
        unicodify = _unicodes.__getitem__

    print(reprfunc(widget), file=file)
    if not isinstance(widget, bananagui.Parent):
        return

    children = list(widget.children())
    for index, child in enumerate(children):
        for character in prefix:
            print(character, end=' '*3, file=file)

        if index == len(children)-1:
            # this is the last child widget
            print(unicodify('`--'), end=' ', file=file)
            new_prefix = prefix + ' '
        else:
            print(unicodify('|--'), end=' ', file=file)
            new_prefix = prefix + unicodify('|')

        _dump_tree(child, file, ascii_only, new_prefix)


# this isn't defined like file=sys.stdout because that doesn't work if
# someone sets sys.stdout to some other file object
def dump(widget, file=None, *, ascii_only=False):
    """Print a tree of a BananaGUI widget and its child widgets.

    The *file* defaults to :data:`sys.stdout`. If *ascii_only* is true,
    :func:`ascii` will be used instead of :func:`repr`.
    """
    if file is None:
        file = sys.stdout
    _dump_tree(widget, file, ascii_only)


def dumps(widget, **kwargs):
    """Like :func:`~dump`, but return a string instead of writing to a file."""
    fakefile = io.StringIO()
    dump(widget, fakefile, **kwargs)
    return fakefile.getvalue()
