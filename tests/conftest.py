import pytest

import bananagui


@pytest.fixture(scope='session')
def dummywrapper():
    bananagui.load('tests.dummywrapper')
