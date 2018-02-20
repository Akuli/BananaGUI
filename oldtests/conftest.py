"""Set up BananaGUI tests."""

import pytest

import bananagui


@pytest.fixture(scope='session')
def dummywrapper():
    # The load() method can't be called twice, so setting up the dummy
    # wrapper and testing load() need to be combined.
    bananagui.WRAPPERS.add('invalid module')
    bananagui.load_wrapper('invalid module', 'dummy')
    bananagui.WRAPPERS.remove('invalid module')
    with pytest.raises(RuntimeError):
        bananagui.load_wrapper('dummy')    # cannot call it twice
