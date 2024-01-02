"""Tests for utils.py."""
import unittest
from hybrid_cc.utils.utils import right, reverse, left


class TestDirectionalUtilities(unittest.TestCase):
    """Test cases for directional utility functions."""

    def test_right(self):
        """Test the 'right' function."""
        self.assertEqual(right('N'), 'E')
        self.assertEqual(right('E'), 'S')
        self.assertEqual(right('S'), 'W')
        self.assertEqual(right('W'), 'N')

    def test_reverse(self):
        """Test the 'reverse' function."""
        self.assertEqual(reverse('N'), 'S')
        self.assertEqual(reverse('E'), 'W')
        self.assertEqual(reverse('S'), 'N')
        self.assertEqual(reverse('W'), 'E')

    def test_left(self):
        """Test the 'left' function."""
        self.assertEqual(left('N'), 'W')
        self.assertEqual(left('E'), 'N')
        self.assertEqual(left('S'), 'E')
        self.assertEqual(left('W'), 'S')


if __name__ == '__main__':
    unittest.main()
