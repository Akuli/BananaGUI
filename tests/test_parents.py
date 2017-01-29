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

"""Test bananagui.widgets.parents."""

import pytest

from bananagui import HORIZONTAL, widgets


def test_child_views(dummywrapper, capsys):
    window = widgets.Window()
    box = widgets.Box()
    window.add(box)
    label1 = widgets.Label("label 1")
    label2 = widgets.Label("label 2")
    box.extend([label1, label2])

    assert window.children == {box}
    assert box.children == {label1, label2}
    assert len(window.children) == 1
    assert len(box.children) == 2
    assert list(window.children) == [box]
    assert list(box.children) == [label1, label2]
    assert box in window.children
    assert None not in window.children
    assert label1 in box.children
    assert label2 in box.children
    assert None not in box.children
    assert repr(window.children) == "<children of a bananagui.widgets.Window>"
    assert repr(box.children) == "<children of a bananagui.widgets.Box>"

    # See _ChildView._from_iterable in bananagui/widgets/parents.py.
    assert type(window.children | {'hi'}) is set
    assert type(box.children | {'there'}) is set

    assert (window.children.__doc__
            == box.children.__doc__
            == widgets.Window.children.__doc__
            == widgets.Box.children.__doc__)


def test_add_and_remove(dummywrapper):
    window1 = widgets.Window("Window 1")
    window2 = widgets.Window("Window 2")
    assert window1.child is window2.child is None
    label = widgets.Label("Label")
    with pytest.raises(ValueError):
        window1.remove(label)  # not added
    window1.add(label)
    with pytest.raises(ValueError):
        window1.add(label)  # already added
    assert window1.child is label
    with pytest.raises(ValueError):
        window1.add(widgets.Button("lol"))  # cannot add two things to a Bin
    window1.remove(label)
    assert window2.child is None
    with pytest.raises(RuntimeError):
        window2.add(label)    # now label has wrong parent


slices = [
    slice(0, 10),
    slice(None, 10, 2),
    slice(0, 10, 100),
    slice(None, None, -1),
    slice(7, 2, -2),
]


def test_box_listyness(dummywrapper):
    labellist = []
    box = widgets.Box()
    for i in range(1, 10):
        label = widgets.Label("Label %d" % i)
        labellist.append(label)
        box.append(label)
    assert box != labellist
    for s in slices:
        assert box[s] == labellist[s]
        temp = labellist[:]
        del box[s]
        del temp[s]
        assert box[:] == temp
        box[:] = labellist  # restore it


def test_box_repr(dummywrapper):
    hbox = widgets.Box(HORIZONTAL)
    vbox = widgets.Box()
    assert repr(hbox) == (
        "<bananagui.widgets.Box object, orient=bananagui.HORIZONTAL, empty>")
    assert repr(vbox) == "<bananagui.widgets.Box object, empty>"
