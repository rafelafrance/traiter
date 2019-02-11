# pylint: disable=missing-docstring,too-many-public-methods

import unittest
from lib.parse import Parse
from lib.traits.sex_trait import SexTrait


PAR = SexTrait()


class TestSexTrait(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('sex=female ?'),
            [Parse(value='female?', start=0, end=12)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('sex=unknown ; crown-rump length=8 mm'),
            [Parse(value='unknown', start=0, end=13)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('sex=F crown rump length=8 mm'),
            [Parse(value='female', start=0, end=5)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('words male female unknown more words'),
            [Parse(value='male', start=6, end=10),
             Parse(value='female', start=11, end=17)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('words male female male more words'),
            [Parse(value='male', start=6, end=10),
             Parse(value='female', start=11, end=17),
             Parse(value='male', start=18, end=22)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('Respective sex and msmt. in mm'),
            [])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('male or female'),
            [Parse(value='male', start=0, end=4),
             Parse(value='female', start=8, end=14)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('sex=unknown length=8 mm'),
            [Parse(value='unknown', start=0, end=11)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('sex=female?'),
            [Parse(value='female?', start=0, end=11)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('sex=not recorded ;'),
            [Parse(value='not recorded', start=0, end=18)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('sex=male ; sex=male ;'),
            [Parse(value='male', start=0, end=10),
             Parse(value='male', start=11, end=21)])
