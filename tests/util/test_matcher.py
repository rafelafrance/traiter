"""Validate the Base matcher class."""

import unittest

from traiter.pylib.util import filter_matches


class TestSpacyMatcher(unittest.TestCase):
    """Test the plant color trait parser."""

    def test_filter_matches_01(self):
        """It handles empty matches."""
        self.assertEqual(filter_matches([]), [])

    def test_filter_matches_02(self):
        """It removes simple overlapping matches."""
        matches = [(None, 1, 2), (None, 0, 2)]
        expect = [(None, 0, 2)]
        self.assertEqual(filter_matches(matches), expect)

    def test_filter_matches_03(self):
        """It removes complicated overlapping matches."""
        matches = [(None, 0, 1), (None, 0, 3), (None, 2, 3)]
        expect = [(None, 0, 3)]
        self.assertEqual(filter_matches(matches), expect)

    def test_filter_matches_04(self):
        """It removes complicated overlapping matches."""
        matches = [(None, 0, 1), (None, 0, 4), (None, 0, 2), (None, 3, 4)]
        expect = [(None, 0, 4)]
        self.assertEqual(filter_matches(matches), expect)

    def test_filter_matches_05(self):
        """It does not remove non-overlapping matches."""
        matches = [(None, 0, 1), (None, 0, 4), (None, 0, 2), (None, 4, 5)]
        expect = [(None, 0, 4), (None, 4, 5)]
        self.assertEqual(filter_matches(matches), expect)
