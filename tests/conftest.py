import pytest

import bananagui


@pytest.fixture(scope='session')
def dummywrapper():
    # The load() method can't be called twice, so setting up the dummy
    # wrapper and testing load() need to be combined.
    bananagui.load('invalid module', 'this is lol', '.dummywrapper')
    with pytest.raises(RuntimeError):
        bananagui.load('.dummywrapper')    # cannot call it twice
