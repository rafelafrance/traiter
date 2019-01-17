import unittest
from lib.parsed_trait import ParsedTrait
from lib.traits.sex import Sex


PAR = Sex()


class TestSex(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('sex=female ?'),
            [ParsedTrait(value='female?', start=0, end=12)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('sex=unknown ; crown-rump length=8 mm'),
            [ParsedTrait(value='unknown', start=0, end=11)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('sex=F crown rump length=8 mm'),
            [ParsedTrait(value='female', start=0, end=5)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('words male female unknown more words'),
            [ParsedTrait(value='male', start=6, end=10),
             ParsedTrait(value='female', start=11, end=17)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('words male female male more words'),
            [ParsedTrait(value='male', start=6, end=10),
             ParsedTrait(value='female', start=11, end=17),
             ParsedTrait(value='male', start=18, end=22)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('Respective sex and msmt. in mm'),
            [])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('male or female'),
            [ParsedTrait(value='male', start=0, end=4),
             ParsedTrait(value='female', start=8, end=14)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('sex=unknown length=8 mm'),
            [ParsedTrait(value='unknown', start=0, end=11)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('sex=female?'),
            [ParsedTrait(value='female?', start=0, end=11)])
