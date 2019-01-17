"""Verify various parts of the base trait class."""

import unittest
from lib.parsers.base import Base, Regexp


class TestBase(unittest.TestCase):
    """Verify various parts of the base trait class."""

    def test_lit_01(self):
        """It builds a regex with a named group."""
        base = Base()
        base.lit('name', 'stuff')
        self.assertEqual(
            base.regexps,
            [Regexp(type='token', name='name', token='001_',
                    regexp='(?P<name> stuff )')])

    def test_lit_02(self):
        """It handles alternation."""
        base = Base()
        base.lit('name', 'stuff | more stuff')
        self.assertEqual(
            base.regexps,
            [Regexp(type='token', name='name', token='001_',
                    regexp='(?P<name> stuff | more stuff )')])

    def test_lit_03(self):
        """It handles numbered repeats."""
        base = Base()
        base.lit('name', '(?: stuff | more stuff){2,3}')
        self.assertEqual(
            base.regexps,
            [Regexp(type='token', name='name', token='001_',
                    regexp='(?P<name> (?: stuff | more stuff){2,3} )')])

    def test_lit_04(self):
        """It renames groups."""
        base = Base()
        base.lit('name', '(?P<grp> stuff )')
        self.assertEqual(
            base.regexps,
            [Regexp(type='token', name='name', token='001_',
                    regexp='(?P<name> (?P<grp_1> stuff ) )')])

    def test_lit_05(self):
        """Every group gets a unique name."""
        base = Base()
        base.lit('name', '(?P<grp> stuff ) (?P<grp> more )')
        self.assertEqual(
            base.regexps,
            [Regexp(
                type='token', name='name', token='001_',
                regexp='(?P<name> (?P<grp_2> stuff ) (?P<grp_1> more ) )')])

    def test_kwd_01(self):
        r"""It surrounds regex with \b delimiters."""
        base = Base()
        base.kwd('name', 'stuff')
        self.assertEqual(
            base.regexps,
            [Regexp(type='token', name='name', token='001_',
                    regexp=r'\b (?P<name> stuff ) \b')])
