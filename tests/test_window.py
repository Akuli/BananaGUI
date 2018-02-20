import functools

import pytest

import bananagui


def test_reprs():
    window = bananagui.Window()
    assert window.title == 'BananaGUI Window'
    assert repr(window) == (
      "<bananagui.Window widget, title='BananaGUI Window', contains nothing>")

    window.close()
    assert repr(window) == (
        "<closed bananagui.Window widget, title was 'BananaGUI Window'>")


def test_close():
    raises_it = functools.partial(
        pytest.raises, RuntimeError, message='the window has been closed')

    window = bananagui.Window()
    assert not window.closed

    window.close()
    assert window.closed
    window.close()
    assert window.closed

    # these are still accessible
    window.title
    window.resizable
    window.hidden

    # not accessible because looked up every time
    with raises_it():
        window.size

    with raises_it():
        window.title = 'toot'
    with raises_it():
        window.resizable = False
    with raises_it():
        window.hidden = True
    with raises_it():
        window.resize(10, 10)
