"""Verify various parts of the base trait class."""

import unittest
from lib.traits.base_trait import BaseTrait
import lib.token as token
import lib.regexp as regexp
from lib.regexp import Regexp


class TestBaseTrait(unittest.TestCase):
    """Verify various parts of the base trait class."""

    @staticmethod
    def reset_globals():
        """Reset the global tiebreakers."""
        regexp.GROUP_COUNT = 0
        token.TOKEN_COUNT = 0

    def setup_method(self, method):
        """Reset the global tiebreakers."""
        self.reset_globals()

    def test_kwd_01(self):
        r"""It surrounds regex with \b delimiters."""
        base = BaseTrait()
        base.kwd('name', 'stuff')
        self.reset_globals()
        self.assertEqual(
            base.regexps,
            {'name': Regexp(
                phase='token', name='name', token='001_',
                regexp=r'\b (?P<name> stuff ) \b')})

    def test_lit_01(self):
        """It builds a regex with a named group."""
        base = BaseTrait()
        base.lit('name', 'stuff')
        self.reset_globals()
        self.assertEqual(
            base.regexps,
            {'name': Regexp(
                phase='token', name='name', token='001_',
                regexp='(?P<name> stuff )')})

    def test_lit_02(self):
        """It handles alternation."""
        base = BaseTrait()
        base.lit('name', 'stuff | more stuff')
        self.reset_globals()
        self.assertEqual(
            base.regexps,
            {'name': Regexp(
                phase='token', name='name', token='001_',
                regexp='(?P<name> stuff | more stuff )')})

    def test_lit_03(self):
        """It handles numbered repeats."""
        base = BaseTrait()
        base.lit('name', '(?: stuff | more stuff){2,3}')
        self.reset_globals()
        self.assertEqual(
            base.regexps,
            {'name': Regexp(
                phase='token', name='name', token='001_',
                regexp='(?P<name> (?: stuff | more stuff){2,3} )')})

    def test_lit_04(self):
        """It renames groups."""
        base = BaseTrait()
        base.lit('name', '(?P<grp> stuff )')
        self.reset_globals()
        self.assertEqual(
            base.regexps,
            {'name': Regexp(
                phase='token', name='name', token='001_',
                regexp='(?P<name> (?P<grp> stuff ) )')})

    def test_lit_05(self):
        """Every group gets a unique name."""
        base = BaseTrait()
        base.lit('name', '(?P<grp> stuff ) (?P<grp> more )')
        self.reset_globals()
        self.assertEqual(
            base.regexps,
            {'name': Regexp(
                phase='token', name='name', token='001_',
                regexp='(?P<name> (?P<grp> stuff ) (?P<grp> more ) )')})
