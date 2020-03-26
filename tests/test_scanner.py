"""Test the scanner."""

import unittest
from traiter.new.scanner import Scanner
from traiter.new.token import Token


class TestScan(unittest.TestCase):
    """Test the scanner'."""

    def test_word_01(self):
        """It finds matches."""
        scanner = Scanner()
        scanner.add(
            'word',
            r' \b (?: \p{Letter}+ \p{Dash_Punctuation}? )* \p{Letter} \b ')
        self.assertEqual(
            scanner.scan('-This is-a test-'),
            [
                Token(text='This', start=1, end=5, genus='word'),
                Token(text='is-a', start=6, end=10, genus='word'),
                Token(text='test', start=11, end=15, genus='word')])
