# pylint: disable=missing-docstring,too-many-public-methods

import unittest
from lib.trait import Trait
from lib.parsers.ear_length import EarLength


PAR = EarLength()


class TestEarLength(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('earLengthInmm: 9'),
            [Trait(value=9, units='mm', start=0, end=16)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('L. 9", T. 4", ear 9/16"'),
            [Trait(value=14.29, units='"', start=14, end=23)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('L. 9", T. 4", HF. 2", E 1",'),
            [Trait(value=25.4, units='"', start=22, end=26)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('{"measurements":"TotalLength=180 Tail=82 '
                      'HindFoot=28 Ear=18" }'),
            [Trait(value=18, flags={'units_inferred': True},
                   start=53, end=59)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('{"earLength":"13", "gonadLength":"3"}'),
            [Trait(value=13, flags={'units_inferred': True},
                   start=2, end=16)])
