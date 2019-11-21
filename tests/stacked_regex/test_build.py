import regex
import unittest
from pylib.stacked_regex.rule import build, replacer, keyword


class TestReplace(unittest.TestCase):

    flags = regex.VERBOSE | regex.IGNORECASE

    r_zero = keyword('zero', r' zero ')
    r_one = keyword('one', r' one ')
    r_two = keyword('two', r' two ')
    r_three = replacer('three', r' zero one ')
    r_four = replacer('four', r' two three ')
    rules = {r.name: r for r in [r_zero, r_one, r_two, r_three, r_four]}

    for rule in [r_three, r_four]:
        rule.regexp = regex.compile(
            build(rule.name, rule.pattern, rules),
            regex.IGNORECASE | regex.VERBOSE)

    def test_build_01(self):
        """It builds a token expression from scanner tokens."""
        actual = build(self.r_three.name, self.r_three.pattern, self.rules)
        expect = r'(?P<three> (?: \b zero; ) (?: \b one; ) )'
        self.assertEqual(actual, expect)

    def test_build_02(self):
        """It builds a token expression from scanner and replacer tokens."""
        actual = build(self.r_four.name, self.r_four.pattern, self.rules)
        expect = (r'(?P<four> (?: \b two; ) ' 
                  r'(?P<three> (?: \b zero; ) (?: \b one; ) ) )')
        self.assertEqual(actual, expect)

    def test_build_03(self):
        """It builds a token expression from replacer tokens."""
        actual = build('five', 'three four', self.rules)
        expect = (r'(?P<five> '
                  r'(?P<three> (?: \b zero; ) (?: \b one; ) ) '
                  r'(?P<four> (?: \b two; ) '
                  r'(?P<three> (?: \b zero; ) (?: \b one; ) ) ) )')
        self.assertEqual(actual, expect)

    def test_build_04(self):
        """It handles names."""
        self.maxDiff = None
        actual = build('six', '(?P<five> three four )', self.rules)
        expect = (r'(?P<six> '
                  r'(?P<five> (?P<three> (?: \b zero; ) (?: \b one; ) ) '
                  r'(?P<four> (?: \b two; ) '
                  r'(?P<three> (?: \b zero; ) (?: \b one; ) ) ) ) )')
        self.assertEqual(actual, expect)

    def test_build_05(self):
        """It handles names."""
        actual = build('six', '(?P<five> zero four )', self.rules)
        expect = (r'(?P<six> '
                  r'(?P<five> (?: \b zero; ) '
                  r'(?P<four> (?: \b two; ) '
                  r'(?P<three> (?: \b zero; ) (?: \b one; ) ) ) ) )')
        self.assertEqual(actual, expect)

    def test_build_06(self):
        """It builds a token expression from duplicate replacer tokens."""
        actual = build('five', 'three three', self.rules)
        expect = (r'(?P<five> '
                  r'(?P<three> (?: \b zero; ) (?: \b one; ) ) '
                  r'(?P<three> (?: \b zero; ) (?: \b one; ) ) )')
        self.assertEqual(actual, expect)
