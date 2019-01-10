# flake8=noqa

import unittest
from lib.parsed_trait import ParsedTrait
from lib.traits.ear_length import EarLength


PAR = EarLength()


class TestEarLength(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('earLengthInmm: 9'),
            [ParsedTrait(value=9, units='earlengthinmm', start=0, end=16)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('L. 9", T. 4", ear 9/16"'),
            [ParsedTrait(value=14.29, units='"', start=14, end=23)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('L. 9", T. 4", HF. 2", E 1",'),
            [ParsedTrait(value=25.4, units='"', start=22, end=26)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('{"measurements":"TotalLength=180 Tail=82 '
                      'HindFoot=28 Ear=18" }'),
            [ParsedTrait(value=18,
                         flags={'units_inferred': True},
                         start=53, end=59)])

    def test_parse_05(self):
        self.assertEqual(
            #          0123456789 123456789 123456789 123456789 123456789
            PAR.parse('{"earLength":"13", "gonadLength":"3"}'),
            [ParsedTrait(value=13,
                         flags={'units_inferred': True},
                         start=2, end=16)])
