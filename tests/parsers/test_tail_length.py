# pylint: disable=missing-docstring,too-many-public-methods

import unittest
from lib.trait import Trait
from lib.parsers.tail_length import TailLength


PAR = TailLength()


class TestTailLength(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('tailLengthInmm: 102'),
            [Trait(value=102, units='mm', start=0, end=19)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('tail length=95 mm;'),
            [Trait(value=95, units='mm', start=0, end=17)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('tail length=95;'),
            [Trait(value=95, flags={'units_inferred': True}, start=0, end=14)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse(', "tail":"92", '),
            [Trait(value=92, flags={'units_inferred': True}, start=3, end=12)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('"tailLengthInMillimeters"="104",'),
            [Trait(value=104, units='millimeters',
                   start=1, end=30)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('measurements:213-91-32-23'),
            [Trait(value=91, units='mm_shorthand', start=0, end=25)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('213-91-32-23'),
            [Trait(value=91, units='mm_shorthand', start=0, end=12)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('taillength=95;'),
            [Trait(value=95, flags={'units_inferred': True}, start=0, end=13)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('reproductive data=testes abdominal; T = 3 x 1.8 ;'),
            [])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('{"measurements":"210-92-30" }'),
            [Trait(value=92, units='mm_shorthand', start=2, end=26)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('measurements:210-92-30 308-190-45-20'),
            [Trait(value=190, units='mm_shorthand', start=23, end=36)])

    def test_parse_12(self):
        self.assertEqual(
            PAR.parse('measurements:210-92-30 185-252 mm'),
            [])
