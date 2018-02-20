import pytest

import bananagui


class Toot:
    pass


def test_fun_reprs():
    callback = bananagui.Callback(int, str, Toot, bananagui.Window)
    assert repr(callback) == str(callback) == (
        'bananagui.Callback(int, str, %s.Toot, bananagui.Window)' % __name__)

    callback = bananagui.Callback(int, str)
    with pytest.raises(TypeError,
                       message="should be run(int, str), not run(str, int)"):
        callback.run('a', 1)
    with pytest.raises(TypeError,
                       message="should be run(int, str), not run(str)"):
        callback.run('a')
    with pytest.raises(TypeError,
                       message=("should be run(int, str), not "
                                "run(bananagui.Window)")):
        callback.run(bananagui.Window())


def test_callback_connecting():
    it_ran = False

    def func(*args):
        assert args == (1, 2, 3)
        nonlocal it_ran
        it_ran = True

    callback = bananagui.Callback(int)
    assert not callback.is_connected(func)

    callback.connect(func)
    assert callback.is_connected(func)
    callback.disconnect(func)
    assert not callback.is_connected(func)

    callback.connect(func, 2, 3)
    assert callback.is_connected(func)
    assert not it_ran
    callback.run(1)
    assert it_ran
    callback.disconnect(func)
    assert not callback.is_connected(func)

    with pytest.raises(ValueError):
        callback.disconnect(func)


def test_connect_multiple():
    callback = bananagui.Callback()
    stuff = []
    callback.connect(stuff.append, 1)
    callback.connect(stuff.append, 2)
    callback.connect(stuff.append, 1.0)
    callback.connect(lambda: stuff.append(100))
    callback.run()
    assert stuff == [1, 2, 1.0, 100]
    assert list(map(type, stuff)) == [int, int, float, int]


def test_blocked():
    def dummy_func():
        nonlocal it_ran
        it_ran = True

    it_ran = False
    callback = bananagui.Callback()
    callback.connect(dummy_func)
    with callback.blocked():
        callback.run()
        with callback.blocked():
            callback.run()
        with pytest.raises(RuntimeError, message=""):
            with callback.blocked():
                raise RuntimeError   # must not screw up this nesting thing
        callback.run()
    assert not it_ran
    callback.run()
    assert it_ran


def test_callback_exc(capsys):
    def broken_func():
        raise LookupError("i can't look up, i'm blind")

    callback = bananagui.Callback()
    callback.connect(broken_func)
    callback.run()
    output, errors = capsys.readouterr()
    assert not output
    assert errors.endswith("\nLookupError: i can't look up, i'm blind\n")

    # the connect line should be added automagically
    assert '\n    callback.connect(broken_func)\n' in errors
