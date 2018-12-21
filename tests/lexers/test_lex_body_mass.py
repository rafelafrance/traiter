import unittest
from lib.lexers.lex_base import Token
from lib.lexers.lex_body_mass import LexBodyMass


LEX = LexBodyMass()


class TestLexBodyMass(unittest.TestCase):

    def test_tokenize_01(self):
        self.assertEqual(
            LEX.tokenize('762-292-121-76 2435.0g'),
            [Token(token='shorthand_mass', start=0, end=22)])

    def test_tokenize_02(self):
        self.assertEqual(
            LEX.tokenize('762:292:121:76=2435.0g'),
            [Token(token='shorthand_mass', start=0, end=22)])

    def test_tokenize_03(self):
        self.assertEqual(
            #             0123456789.123456789.123456789.123456789.
            LEX.tokenize('762:292:121:76=2435.0 grams'),
            [Token(token='shorthand_mass', start=0, end=27)])

    def test_tokenize_04(self):
        self.assertEqual(
            #             0123456789.123456789.123456789.123456789.
            LEX.tokenize('1982-10-12'),
            [])
