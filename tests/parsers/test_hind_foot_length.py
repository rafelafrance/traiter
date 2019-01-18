# pylint: disable=missing-docstring,too-many-public-methods

import unittest
from lib.trait import Trait
from lib.parsers.hind_foot_length import HindFootLength


PAR = HindFootLength()


class TestHindFootLength(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('hind foot with claw=30 mm;'),
            [Trait(value=30, units='mm', start=0, end=25)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('"hindfootLengthInMM":"36"'),
            [Trait(value=36, units='hindfootlengthinmm', start=1, end=24)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('"hind foot length":"34.0"'),
            [Trait(value=34, flags={'units_inferred': True}, start=1, end=24)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('; HindFoot: 30.0; '),
            [Trait(value=30, flags={'units_inferred': True}, start=2, end=16)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('{"measurements":"192-84-31-19=38g" }'),
            [Trait(value=31, units='mm_shorthand', start=2, end=33)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('{"measurements":"192-84-[31]-19=38g" }'),
            [Trait(value=31, units='mm_shorthand',
                   flags={'estimated_value': True},
                   start=2, end=35)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('T: 98.5, HF: 29 ;'),
            [Trait(value=29, flags={'units_inferred': True}, start=9, end=15)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('T-94mm, HF-30mm, E/n-19mm,'),
            [Trait(value=30, units='mm', start=8, end=15)])
