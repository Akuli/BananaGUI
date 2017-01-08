# Copyright (c) 2017 Akuli

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

"""Print a tree of a widget and its child widgets.

Example:

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
you can use bananagui.iniloader:

    $ iniloader tree thefile.ini
"""
# Unfortunately there isn't a good way to require pytest fixtures from
# doctests, so the docstring isn't tested.

import io
import sys

from bananagui import widgets


def _clean_repr(obj, ascii_only):
    if ascii_only:
        result = ascii(obj)
    else:
        result = repr(obj)
    if result.startswith('<') and result.endswith('>'):
        result = result[1:-1]
    return result


def _dump_tree(widget, file, ascii_only, prefix=''):
    children = list(widget.iter_children())
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


def dump(widget, *, file=None, ascii_only=False):
    """Print a tree of a parent widget and its child widgets.

    The file defaults to sys.stdout. If ascii_only is true, no
    non-ascii characters will be used.
    """
    if not isinstance(widget, widgets.Parent):
        raise TypeError("expected a Parent widget, got %r" % (widget,))
    # This allows monkeypatching sys.stdout.
    if file is None:
        file = sys.stdout
    print(_clean_repr(widget, ascii_only), file=file)
    _dump_tree(widget, file, ascii_only)


def dumps(widget, **kwargs):
    """Like dump(), but return a string instead of printing to a file."""
    fakefile = io.StringIO()
    dump(widget, file=fakefile, **kwargs)
    return fakefile.getvalue()
