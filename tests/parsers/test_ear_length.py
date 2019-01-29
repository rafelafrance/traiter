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
            [Trait(value=25.4, units='"', flags={'ambiguous_char': True},
                   start=22, end=26)])

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

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('ear tag 570'),
            [])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('verbatim collector=E. E. Makela 2432 ; sex=female'),
            [])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('grid 9, station E1.'),
            [])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('ear from notch=17 mm;'),
            [Trait(value=17, units='mm', flags={'measured_from': 'notch'},
                   start=0, end=20)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('earfromcrown=17mm;'),
            [Trait(value=17, units='mm', flags={'measured_from': 'crown'},
                   start=0, end=17)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('{"measurements":"242-109-37-34=N/D" }'),
            [Trait(value=34, units='mm_shorthand', start=2, end=34)])

    def test_parse_12(self):
        self.assertEqual(
            PAR.parse('E/n-21mm'),
            [Trait(value=21, units='mm',
                   flags={'ambiguous_char': True, 'measured_from': 'n'},
                   start=0, end=8)])

    def test_parse_13(self):
        self.assertEqual(
            PAR.parse('E/c-21mm'),
            [Trait(value=21, units='mm',
                   flags={'ambiguous_char': True, 'measured_from': 'c'},
                   start=0, end=8)])
