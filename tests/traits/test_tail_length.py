# flake8=noqa

import unittest
from lib.parsed_trait import ParsedTrait
from lib.traits.tail_length import TailLength


PAR = TailLength()


class TestTailLength(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('tailLengthInmm: 102'),
            [ParsedTrait(
                value=102,
                units='taillengthinmm',
                start=0, end=19)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('tail length=95 mm;'),
            [ParsedTrait(value=95, units='mm', start=0, end=17)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('tail length=95;'),
            [ParsedTrait(
                value=95,
                flags={'units_inferred': True},
                start=0, end=14)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse(', "tail":"92", '),
            [ParsedTrait(
                value=92,
                flags={'units_inferred': True},
                start=3, end=12)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('"tailLengthInMillimeters"="104",'),
            [ParsedTrait(
                value=104,
                units='taillengthinmillimeters',
                start=1, end=30)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('measurements:213-91-32-23'),
            [ParsedTrait(value=91, units='mm_shorthand', start=0, end=25)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('213-91-32-23'),
            [ParsedTrait(value=91, units='mm_shorthand', start=0, end=12)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('taillength=95;'),
            [ParsedTrait(
                value=95,
                flags={'units_inferred': True},
                start=0, end=13)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('reproductive data=testes abdominal; T = 3 x 1.8 ;'),
            [])
