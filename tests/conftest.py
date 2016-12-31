import pytest

import bananagui


@pytest.fixture(scope='session')
def dummywrapper():
    # The load() method can't be called twice, so setting up the dummy
    # wrapper and testing it need to be combined.
    bananagui.load('invalid-module', 'this-is-lol', 'tests.dummywrapper')
    with pytest.raises(RuntimeError):
        bananagui.load('tests.dummywrapper')    # cannot call it twice
