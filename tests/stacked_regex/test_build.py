"""Test the build function for the rules object."""

import unittest
import regex
from pylib.stacked_regex.rule import grouper, vocab


class TestReplace(unittest.TestCase):
    """Test the build function for the rules object."""

    flags = regex.VERBOSE | regex.IGNORECASE

    r_zero = vocab('zero', r' zero ')
    r_one = vocab('one', r' one ')
    r_two = vocab('two', r' two ')
    r_three = grouper('three', r' zero one ')
    r_four = grouper('four', r' two three ')
    r_five = grouper('five', r' three four ')
    rules = {r.name: r for r in [r_zero, r_one, r_two, r_three, r_four]}

    for rule in [r_three, r_four]:
        rule.compile(rules)

    def test_build_01(self):
        """It builds a token expression from scanner tokens."""
        actual = self.r_three.build(self.rules)
        expect = r'(?P<three> (?: \b zero; ) (?: \b one; ) )'
        self.assertEqual(actual, expect)

    def test_build_02(self):
        """It builds a token expression from scanner and grouper tokens."""
        actual = self.r_four.build(self.rules)
        expect = (r'(?P<four> (?: \b two; ) '
                  r'(?P<three> (?: \b zero; ) (?: \b one; ) ) )')
        self.assertEqual(actual, expect)

    def test_build_03(self):
        """It builds a token expression from grouper tokens."""
        actual = self.r_five.build(self.rules)
        expect = (r'(?P<five> '
                  r'(?P<three> (?: \b zero; ) (?: \b one; ) ) '
                  r'(?P<four> (?: \b two; ) '
                  r'(?P<three> (?: \b zero; ) (?: \b one; ) ) ) )')
        self.assertEqual(actual, expect)

    def test_build_04(self):
        """It handles names."""
        r_six = grouper('six', r' (?P<five> three four ) ')
        actual = r_six.build(self.rules)
        expect = (r'(?P<six> '
                  r'(?P<five> (?P<three> (?: \b zero; ) (?: \b one; ) ) '
                  r'(?P<four> (?: \b two; ) '
                  r'(?P<three> (?: \b zero; ) (?: \b one; ) ) ) ) )')
        self.assertEqual(actual, expect)

    def test_build_05(self):
        """It handles names."""
        r_six = grouper('six', r' (?P<five> zero four ) ')
        actual = r_six.build(self.rules)
        expect = (r'(?P<six> '
                  r'(?P<five> (?: \b zero; ) '
                  r'(?P<four> (?: \b two; ) '
                  r'(?P<three> (?: \b zero; ) (?: \b one; ) ) ) ) )')
        self.assertEqual(actual, expect)

    def test_build_06(self):
        """It builds a token expression from duplicate grouper tokens."""
        r_six = grouper('six', r' three three ')
        actual = r_six.build(self.rules)
        expect = (r'(?P<six> '
                  r'(?P<three> (?: \b zero; ) (?: \b one; ) ) '
                  r'(?P<three> (?: \b zero; ) (?: \b one; ) ) )')
        self.assertEqual(actual, expect)
