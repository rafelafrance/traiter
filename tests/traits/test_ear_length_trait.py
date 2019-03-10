# pylint: disable=missing-docstring,too-many-public-methods

import unittest
from lib.parse import Parse
from lib.traits.ear_length_trait import EarLengthTrait


PAR = EarLengthTrait()


class TestEarLengthTrait(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('earLengthInmm: 9'),
            [Parse(value=9, units='mm', start=0, end=16)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('L. 9", T. 4", ear 9/16"'),
            [Parse(value=14.29, units='"', start=14, end=23)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('L. 9", T. 4", HF. 2", E 1",'),
            [Parse(value=25.4, units='"', ambiguous_key=True,
                   start=22, end=26)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('{"measurements":"TotalLength=180 Tail=82 '
                      'HindFoot=28 Ear=18" }'),
            [Parse(value=18, units_inferred=True, start=53, end=59)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('{"earLength":"13", "gonadLength":"3"}'),
            [Parse(value=13, units_inferred=True,
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
            [Parse(value=17, units='mm', measured_from='notch',
                   start=0, end=20)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('earfromcrown=17mm;'),
            [Parse(value=17, units='mm', measured_from='crown',
                   start=0, end=17)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('{"measurements":"242-109-37-34=N/D" }'),
            [Parse(value=34, units='mm_shorthand', start=2, end=34)])

    def test_parse_12(self):
        self.assertEqual(
            PAR.parse('E/n-21mm'),
            [Parse(value=21, units='mm', ambiguous_key=True,
                   measured_from='n', start=0, end=8)])

    def test_parse_13(self):
        self.assertEqual(
            PAR.parse('E/c-21mm'),
            [Parse(value=21, units='mm', ambiguous_key=True,
                   measured_from='c', start=0, end=8)])

    def test_parse_14(self):
        self.assertEqual(
            PAR.parse('; ear from notch=.25 in'),
            [Parse(value=6.35, units='in', measured_from='notch',
                   start=2, end=23)])

    def test_parse_15(self):
        self.assertEqual(
            PAR.parse('"relatedresourceid": '
                      '"99846657-2832-4987-94cd-451b9679725c"'),
            [])

    def test_parse_16(self):
        self.assertEqual(
            PAR.parse('"356142E 4805438N. Very small"'),
            [])

    def test_parse_17(self):
        # self.maxDiff = None
        self.assertEqual(
            PAR.parse('Hind Foot: 19 EFN: 13 Weight: 16.3'),
            [Parse(value=13, measured_from='n', units_inferred=True,
                   start=14, end=21)])
