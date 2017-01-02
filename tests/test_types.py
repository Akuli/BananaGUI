# Copyright (c) 2016-2017 Akuli

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

import pytest

from bananagui import types


# @add_callback
# ~~~~~~~~~~~~~

@types.add_callback('on_stuff')
class CallbackDummy:

    def __init__(self, the_repr='<the dummy>'):
        self._repr = the_repr

    def __repr__(self):
        return self._repr


def test_callback_repr():
    # must be compatible with both of these common repr styles
    dummy1 = CallbackDummy()
    dummy2 = CallbackDummy('Dummy(1, 2, 3)')
    assert (repr(dummy1.on_stuff) == str(dummy1.on_stuff)
            == "<BananaGUI callback 'on_stuff' of the dummy>")
    assert (repr(dummy2.on_stuff) == str(dummy2.on_stuff)
            == "<BananaGUI callback 'on_stuff' of Dummy(1, 2, 3)>")


def test_callback_connecting():
    def func(*args):
        assert args == (1, 2, 3)
        nonlocal it_ran
        it_ran = True

    it_ran = False
    dummy = CallbackDummy()
    assert not dummy.on_stuff.is_connected(func)

    dummy.on_stuff.connect(func)
    assert dummy.on_stuff.is_connected(func)
    dummy.on_stuff.disconnect(func)
    assert not dummy.on_stuff.is_connected(func)

    dummy.on_stuff.connect(func, 1, 2, 3)
    assert dummy.on_stuff.is_connected(func)
    assert not it_ran
    dummy.on_stuff.run()
    assert it_ran
    dummy.on_stuff.disconnect(func)
    assert not dummy.on_stuff.is_connected(func)

    with pytest.raises(ValueError):
        dummy.on_stuff.disconnect(func)


def test_connect_args():
    def func(*args):
        assert args == (1, 2, 3)
        nonlocal it_ran
        it_ran = True

    it_ran = False
    dummy = CallbackDummy()
    dummy.on_stuff.connect(func, 1, 2, 3)
    assert dummy.on_stuff.is_connected(func)
    dummy.on_stuff.run()
    assert it_ran


def test_callback_blocked():
    def dummy_func():
        nonlocal it_ran
        it_ran = True

    it_ran = False
    dummy = CallbackDummy()
    dummy.on_stuff.connect(dummy_func)
    with dummy.on_stuff.blocked():
        dummy.on_stuff.run()
        with dummy.on_stuff.blocked():
            dummy.on_stuff.run()
        try:
            with dummy.on_stuff.blocked():
                raise RuntimeError  # must not screw up this nesting thing
        except RuntimeError:
            pass
        dummy.on_stuff.run()
    assert not it_ran
    dummy.on_stuff.run()
    assert it_ran


def test_callback_exc(capsys):
    def broken_callback():
        raise Exception("oops!")

    dummy = CallbackDummy()
    dummy.on_stuff.connect(broken_callback)
    dummy.on_stuff.run()
    output, errors = capsys.readouterr()
    assert not output
    assert errors.endswith('Exception: oops!\n')
    # The connect line should be added automagically.
    assert 'dummy.on_stuff.connect(broken_callback)' in errors


# @add_property
# ~~~~~~~~~~~~~

class DummyWrapper:

    def __init__(self, dummy):
        self._dummy = dummy

    def set_string(self, string):
        # It should already be set.
        assert self._dummy._string == self._dummy.string == string

    def set_intpair(self, intpair):
        assert self._dummy._intpair == self._dummy.intpair == intpair

    def set_thingy(self, thingy):
        print("setting thingy to", thingy)


@types.add_property('intpair', allow_none=True, how_many=2,
                    minimum=0, maximum=10)
@types.add_property('string', add_changed=True, type=str)
@types.add_property('thingy', choices=(1, 2), extra_setter=print)
class Dummy:

    def __init__(self):
        self._wrapper = DummyWrapper(self)
        self._string = 'a'
        self._intpair = (1, 2)
        self._thingy = 1

    def __repr__(self):
        return '<the dummy>'


def test_add_property_errors():
    d = Dummy()
    with pytest.raises(TypeError):
        d.intpair = iter([1, 2])    # needs to be a sequence
    with pytest.raises(TypeError):
        d.intpair = None
    with pytest.raises(ValueError):
        d.intpair = (1, 2, 3)   # needs to be of length 2
    d.intpair = (None, None)
    d.intpair = [2, 4]
    with pytest.raises(TypeError):
        d.intpair = {2, 4}      # must be a sequence
    with pytest.raises(ValueError):
        d.string = None
    with pytest.raises(TypeError):
        d.string = 123
    with pytest.raises(TypeError):
        d.intpair = ('hello', 'there')
    with pytest.raises(ValueError):
        d.thingy = 3
    d.intpair = (0, 10)
    with pytest.raises(ValueError):
        d.intpair = (-1, 10)
    with pytest.raises(ValueError):
        d.intpair = (0, 11)


def test_wrapper_set(capsys):
    d = Dummy()
    d.thingy = 2
    output, errors = capsys.readouterr()
    assert not errors
    assert output == (
        '<the dummy> 2\n'        # from extra_setter=print
        'setting thingy to 2\n'  # from DummyWrapper.set_thingy
    )
