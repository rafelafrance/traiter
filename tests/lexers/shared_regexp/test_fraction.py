import unittest
from lib.lexers.lex_base import LexBase
import lib.lexers.shared_regexp as regexp


LEX = LexBase()
LEX.lex_rules = [regexp.fraction, regexp.number, regexp.word, regexp.sep]
LEX.build_regex()


class TestRange(unittest.TestCase):

    def compare_tokens(self, text, expect):
        tokens = LEX.tokenize(text)
        actual = [(t.token, text[t.start:t.end]) for t in tokens]
        self.assertEqual(actual, expect)

    def test_fraction_01(self):
        text = '1/2'
        expect = [('fraction', '1/2')]
        self.compare_tokens(text, expect)

    def test_fraction_02(self):
        text = '1 2/3'
        expect = [('fraction', '1 2/3')]
        self.compare_tokens(text, expect)

    def test_fraction_03(self):
        text = '1.0 2/3'
        expect = [('number', '1.0'), ('fraction', '2/3')]
        self.compare_tokens(text, expect)

    def test_fraction_04(self):
        text = '1 2.0/3'
        expect = [('number', '1'), ('number', '2.0'), ('number', '3')]
        self.compare_tokens(text, expect)

    def test_fraction_05(self):
        text = '2012/4/5'
        expect = [('number', '2012'), ('number', '4'), ('number', '5')]
        self.compare_tokens(text, expect)

    def test_fraction_06(self):
        text = '1/2/'
        expect = [('number', '1'), ('number', '2')]
        self.compare_tokens(text, expect)

    def test_fraction_07(self):
        text = '/1/2'
        expect = [('number', '1'), ('number', '2')]
        self.compare_tokens(text, expect)

    def test_fraction_08(self):
        text = '1/'
        expect = [('number', '1')]
        self.compare_tokens(text, expect)
