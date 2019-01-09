# flake8=noqa

import unittest
from lib.parse_result import ParseResult
from lib.traits.hind_foot_length import HindFootLength


PAR = HindFootLength()


class TestHindFootLength(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('hind foot with claw=30 mm;'),
            [ParseResult(value=30, units='mm', start=0, end=25)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('"hindfootLengthInMM":"36"'),
            [ParseResult(
                value=36, units='hindfootlengthinmm', start=1, end=24)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('"hind foot length":"34.0"'),
            [ParseResult(
                value=34, flags={'units_inferred': True}, start=1, end=24)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('; HindFoot: 30.0; '),
            [ParseResult(
                value=30, flags={'units_inferred': True}, start=2, end=16)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('{"measurements":"192-84-31-19=38g" }'),
            [ParseResult(
                value=31, units='mm_shorthand', start=2, end=33)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('{"measurements":"192-84-[31]-19=38g" }'),
            [ParseResult(
                value=31,
                units='mm_shorthand',
                flags={'estimated_value': True},
                start=2, end=35)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('T: 98.5, HF: 29 ;'),
            [ParseResult(
                value=29, flags={'units_inferred': True}, start=9, end=15)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('T-94mm, HF-30mm, E/n-19mm,'),
            [ParseResult(value=30, units='mm', start=8, end=15)])
