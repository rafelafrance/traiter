import unittest
from lib.lexers.lex_base import LexBase
import lib.lexers.shared_regexp as regexp


LEX = LexBase()
LEX.lex_rules = [regexp.number, regexp.word, regexp.sep]
LEX.build_regex()


class TestNumber(unittest.TestCase):

    def compare_tokens(self, text, expect):
        tokens = LEX.tokenize(text)
        actual = [(t.token, text[t.start:t.end]) for t in tokens]
        self.assertEqual(actual, expect)

    def test_number_01(self):
        text = '0'
        expect = [('number', '0')]
        self.compare_tokens(text, expect)

    def test_number_02(self):
        text = '1.'
        expect = [('number', '1'), ('sep', '.')]
        self.compare_tokens(text, expect)

    def test_number_03(self):
        text = '1.1'
        expect = [('number', '1.1')]
        self.compare_tokens(text, expect)

    def test_number_04(self):
        text = '0.1'
        expect = [('number', '0.1')]
        self.compare_tokens(text, expect)

    def test_number_05(self):
        text = '0,1'
        expect = [('number', '0'), ('number', '1')]
        self.compare_tokens(text, expect)

    def test_number_06(self):
        text = '12,3'
        expect = [('number', '12'), ('number', '3')]
        self.compare_tokens(text, expect)

    def test_number_07(self):
        text = '123,4'
        expect = [('number', '123'), ('number', '4')]
        self.compare_tokens(text, expect)

    def test_number_08(self):
        text = '1,234'
        expect = [('number', '1,234')]
        self.compare_tokens(text, expect)

    def test_number_09(self):
        text = '1,234.'
        expect = [('number', '1,234'), ('sep', '.')]
        self.compare_tokens(text, expect)

    def test_number_10(self):
        text = '1,234.5'
        expect = [('number', '1,234.5')]
        self.compare_tokens(text, expect)

    def test_number_11(self):
        text = '1,234.5.'
        expect = [('number', '1,234.5'), ('sep', '.')]
        self.compare_tokens(text, expect)

    def test_number_12(self):
        text = '1,234,5.'
        expect = [('number', '1,234'), ('number', '5'), ('sep', '.')]
        self.compare_tokens(text, expect)

    def test_number_13(self):
        text = '12345'
        expect = [('number', '12345')]
        self.compare_tokens(text, expect)

    def test_number_14(self):
        text = '12345.'
        expect = [('number', '12345'), ('sep', '.')]
        self.compare_tokens(text, expect)

    def test_number_15(self):
        text = '12345.6'
        expect = [('number', '12345.6')]
        self.compare_tokens(text, expect)
