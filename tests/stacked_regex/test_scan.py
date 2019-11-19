import unittest
from pylib.stacked_regex.rule import fragment
from pylib.stacked_regex.token import Token
from pylib.stacked_regex.parser import scan


class TestScan(unittest.TestCase):

    r_dog = fragment('dog', ' doggie dog '.split())
    r_cat = fragment('cat', ' bearcat cat '.split())

    def test_scan_01(self):
        """It finds a match."""
        self.assertEqual(
            scan([self.r_dog], 'dogs'),
            [Token(self.r_dog, span=(0, 3), groups={'dog': 'dog'})])

    def test_scan_02(self):
        """It compares with another token object."""
        self.assertEqual(scan([self.r_dog], 'dogs'), scan([self.r_dog], 'dog'))

    def test_scan_03(self):
        """It finds multiple tokens."""
        self.assertEqual(
            scan([self.r_dog], 'doggie dogs'),
            [Token(self.r_dog, span=(0, 6), groups={'dog': 'doggie'}),
             Token(self.r_dog, span=(7, 10), groups={'dog': 'dog'})])

    def test_scan_04(self):
        """It skips strings that are part of a previous token."""
        self.assertEqual(
            scan([self.r_cat], 'bearcat cats'),
            [Token(self.r_cat, span=(0, 7), groups={'cat': 'bearcat'}),
             Token(self.r_cat, span=(8, 11), groups={'cat': 'cat'})])
