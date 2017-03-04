import pytest

from bananagui import images


def test_image_errors():
    with pytest.raises(ValueError):
        images.Image.from_size(-1, -1)
