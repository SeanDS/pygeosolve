import unittest
import random
from pygeosolve.geometry import Point

class TestValidPoint(unittest.TestCase):
    """Tests for valid point."""

    x = None
    """x-coordinate to use for tests."""

    y = None
    """y-coordinate to use for tests."""

    point = None
    """Point object to use for tests."""

    def setUp(self):
        # random x- and y-values
        self.x = random.uniform(-1, 1)
        self.y = random.uniform(-1, 1)

        # create the point
        self.point = Point(self.x, self.y)

    def test_init(self):
        """Test valid constructor inputs."""

        # check that x and y don't change
        self.assertEqual(self.point.x, self.x)
        self.assertEqual(self.point.y, self.y)

    def test_params(self):
        """Test extraction of parameters."""

        # check parameter list is as expected
        self.assertEqual(self.point.params(), [self.x, self.y])

    def test_str(self):
        """Test string representation."""

        # check string representation is as expected
        self.assertEqual(str(self.point), "({0}, {1})".format(self.x, self.y))

if __name__ == '__main__':
    unittest.main()
