import pytest

from bananagui import color


def test_errors():
    with pytest.raises(ValueError):
        color.hex2rgb('#')
    with pytest.raises(ValueError):
        color.hex2rgb('afff')
    with pytest.raises(ValueError):
        color.hex2rgb('#ffff')
    with pytest.raises(ValueError):
        color.rgbstring2hex('aaaaaa')
