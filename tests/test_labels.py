import bananagui


def test_repr():
    label = bananagui.Label()
    assert repr(label) == "<bananagui.Label widget, text=''>"
