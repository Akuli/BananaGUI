import pytest

from bananagui import types


# @add_callback
# ~~~~~~~~~~~~~

@types.add_callback('on_stuff', doc="on_stuff doc")
class CallbackDummy:
    pass


def test_callback_repr():
    dummy = CallbackDummy()
    should_be = ("<BananaGUI callback 'on_stuff' of %s.CallbackDummy object>"
                 % __name__)
    assert repr(dummy.on_stuff) == str(dummy.on_stuff) == should_be


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
        assert self._dummy._prop_string == self._dummy.string == string

    def set_intpair(self, intpair):
        assert self._dummy._prop_intpair == self._dummy.intpair == intpair

    def set_thingy(self, thingy):
        print("setting thingy to", thingy)


@types.add_property('intpair', allow_none=True, how_many=2,
                    minimum=0, maximum=10, doc="intpair doc")
@types.add_property('string', add_changed=True, type=str, doc="string doc")
@types.add_property('thingy', choices=(1, 2), extra_setter=print,
                    doc="thingy doc")
class WrapperDummy:

    def __init__(self):
        self._wrapper = DummyWrapper(self)
        self._prop_string = 'a'
        self._prop_intpair = (1, 2)
        self._prop_thingy = 1

    def __repr__(self):
        return '<the WrapperDummy>'


def test_add_property_errors():
    d = WrapperDummy()
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
    d = WrapperDummy()
    d.thingy = 2
    output, errors = capsys.readouterr()
    assert not errors
    assert output == (
        '<the WrapperDummy> 2\n'        # from extra_setter=print
        'setting thingy to 2\n'  # from DummyWrapper.set_thingy
    )


# Misc stuff
# ~~~~~~~~~~

def test_docs(capsys):
    pairs = [
        # (descriptor, doc), ...
        (CallbackDummy.on_stuff, "on_stuff doc"),
        (WrapperDummy.intpair, "intpair doc"),
        (WrapperDummy.string, "string doc"),
        (WrapperDummy.thingy, "thingy doc"),
    ]
    for descriptor, doc in pairs:
        assert descriptor.__doc__ == doc
        help(descriptor)
        output, errors = capsys.readouterr()
        assert doc in output
        assert not errors
