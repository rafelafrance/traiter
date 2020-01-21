"""Test the tricky parts of the HTML writer."""

import re
import unittest
from traiter_efloras.writers.html_writer import Cut, insert_markup


class TestHtmlWriter(unittest.TestCase):
    """Test the tricky parts in the module."""

    @staticmethod
    def tags():
        """Create tags used for tests."""
        return {
            (1, True): '[', (1, False): ']', (2, True): '<', (2, False): '>'}

    @staticmethod
    def cuts(text):
        """
        Set up the cuts based on the input text.

        The input code:
            1: Means that the position is for a type 1 only
            2: Means that the position is for a type 2 only
            n: Means that the position is for both type 1 and type 2
        """
        cuts = []
        match1 = re.search(r'[1n]+', text)
        match2 = re.search(r'[2n]+', text)
        cuts.append(Cut(
            pos=match1.start(), open=True,
            len=-(match1.end() - match1.start()), id=-1, end=match1.end(),
            type=1))
        cuts.append(Cut(
            pos=match1.end(), open=False, len=match1.end() - match1.start(),
            id=1, end=match1.end(), type=1))
        cuts.append(Cut(
            pos=match2.start(), open=True,
            len=-(match2.end() - match2.start()), id=-2, end=match2.end(),
            type=2))
        cuts.append(Cut(
            pos=match2.end(), open=False, len=match2.end() - match2.start(),
            id=2, end=match2.end(), type=2))
        return cuts

    def test_insert_markup_01(self):
        """Test no overlap and no shared borders."""
        text = '1111..2222'
        self.assertEqual(
            insert_markup(text, self.cuts(text), self.tags()),
            '[1111]..<2222>')

    def test_insert_markup_02(self):
        """Test no overlap and an adjoining border."""
        text = '.11112222.'
        self.assertEqual(
            insert_markup(text, self.cuts(text), self.tags()),
            '.[1111]<2222>.')

    def test_insert_markup_03(self):
        """Test one is contained in another."""
        text = '.11nnnn11.'
        self.assertEqual(
            insert_markup(text, self.cuts(text), self.tags()),
            '.[11<nnnn>11].')

    def test_insert_markup_04(self):
        """Test both have the same span."""
        text = '.nnnnnn.'
        self.assertEqual(
            insert_markup(text, self.cuts(text), self.tags()),
            '.<[nnnnnn]>.')

    def test_insert_markup_05(self):
        """Test if the cuts both end at same pos but have different lengths."""
        text = '.11nnnn.'
        self.assertEqual(
            insert_markup(text, self.cuts(text), self.tags()),
            '.[11<nnnn>].')

    def test_insert_markup_06(self):
        """Test if the cuts both end at same pos but have different lengths."""
        text = '22nnnn.'
        self.assertEqual(
            insert_markup(text, self.cuts(text), self.tags()),
            '<22[nnnn]>.')

    def test_insert_markup_07(self):
        """Test if cuts both start at same pos but are different lengths."""
        text = '.nnnn11.'
        self.assertEqual(
            insert_markup(text, self.cuts(text), self.tags()),
            '.[<nnnn>11].')

    def test_insert_markup_08(self):
        """Test if cuts both start at same pos but are different lengths."""
        text = 'nnnn22.'
        self.assertEqual(
            insert_markup(text, self.cuts(text), self.tags()),
            '<[nnnn]22>.')

    def test_insert_markup_09(self):
        """Test if the cuts overlap in a non-html compliant way."""
        text = '.11nn22.'
        self.assertEqual(
            insert_markup(text, self.cuts(text), self.tags()),
            '.[11<nn>]<22>.')

    def test_insert_markup_10(self):
        """Test if the cuts overlap in a non-html compliant way."""
        text = '.22nn11.'
        self.assertEqual(
            insert_markup(text, self.cuts(text), self.tags()),
            '.<22[nn]>[11].')
