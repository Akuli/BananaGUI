"""Test bananagui.widgets.parents."""

import pytest

from bananagui import Orient, widgets


def test_children(dummywrapper, capsys):
    window = widgets.Window()
    box = widgets.Box()
    window.add(box)
    label1 = widgets.Label("label 1")
    label2 = widgets.Label("label 2")
    box.extend([label1, label2])

    pairs = [
        # (widget, children)
        (window, [box]),
        (box, [label1, label2]),
    ]
    for widget, children in pairs:
        assert list(widget.children()) == children

    assert (window.children.__doc__
            == box.children.__doc__
            == widgets.Parent.children.__doc__
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
    hbox = widgets.Box(Orient.HORIZONTAL)
    vbox = widgets.Box()
    assert repr(hbox) == (
        "<bananagui.widgets.Box object, horizontal, empty>")
    assert repr(vbox) == "<bananagui.widgets.Box object, empty>"
