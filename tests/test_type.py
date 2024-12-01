import pytest
import PIL
from PIL import Image
from pathlib import Path


class Equality:
    """Class to test equality comparisons."""
    def __init__(self, val):
        self.val = val

    def __eq__(self, other):
        if not isinstance(other, Equality):
            return NotImplemented
        return self.val == other.val


class UnitTest:
    """Class containing type checking utilities."""
    def is_image(self, src):
        """Check if input is a PIL Image instance."""
        return isinstance(src, PIL.Image.Image)

    def is_list(self, src):
        """Check if input is a list instance."""
        return isinstance(src, list)


@pytest.fixture
def test_image_path():
    """Fixture providing test image path."""
    return Path('src/data/input/1922/1922-022.png')


def test_image(test_image_path):
    """Test PIL image type checking."""
    unittest = UnitTest()
    inp = PIL.Image.open(test_image_path)
    assert unittest.is_image(inp)


def test_list():
    """Test list type checking."""
    unittest = UnitTest()
    test_list = [1, 2, 3]
    assert unittest.is_list(test_list)
    assert not unittest.is_list("not a list")


def test_equality():
    """Test Equality class comparison."""
    f1 = Equality(1)
    f2 = Equality(1)
    f3 = Equality(2)
    
    assert f1 == f2
    assert f1 != f3
