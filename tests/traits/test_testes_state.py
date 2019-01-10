# flake8=noqa

import unittest
from lib.parsed_trait import ParsedTrait
from lib.traits.testes_state import TestesState


PAR = TestesState()


class TestTestesState(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('some words reproductive data=No testicles; more words'),
            [ParsedTrait(value='no testicles', start=11, end=41)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('testes descended'),
            [ParsedTrait(value='descended', start=0, end=16)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('testes undescended'),
            [ParsedTrait(value='undescended', start=0, end=18)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('testes undesc.'),
            [ParsedTrait(value='undesc', start=0, end=13)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('testes undesc'),
            [ParsedTrait(value='undesc', start=0, end=13)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('testes not fully descended'),
            [ParsedTrait(value='not fully descended', start=0, end=26)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('testes not-scrotal'),
            [ParsedTrait(value='not scrotal', start=0, end=18)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('testes no scrotum'),
            [ParsedTrait(value='no scrotum', start=0, end=17)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('testis nscr'),
            [ParsedTrait(value='nscr', start=0, end=11)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('testes ns'),
            [ParsedTrait(value='ns', start=0, end=9)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('tes undescend.'),
            [ParsedTrait(value='undescend', start=0, end=13)])

    def test_parse_12(self):
        self.assertEqual(
            PAR.parse('t abdominal'),
            [ParsedTrait(value='abdominal', start=0, end=11)])

    def test_parse_13(self):
        self.assertEqual(
            PAR.parse('t nscr'),
            [ParsedTrait(value='nscr', start=0, end=6)])

    def test_parse_14(self):
        self.assertEqual(
            PAR.parse('t ns'),
            [])

    def test_parse_15(self):
        self.assertEqual(
            PAR.parse(
                ('hind foot with claw=35 mm; '
                 'reproductive data=Testes partially descended. '
                 'Sperm present.')),
            [ParsedTrait(value='partially descended', start=27, end=71)])

    def test_parse_16(self):
        self.assertEqual(
            PAR.parse(
                ('sex=male ; reproductive data=testis 5mm, abdominal '
                 '; ear from notch=20 mm; ')),
            [ParsedTrait(value='abdominal', start=11, end=50)])

    def test_parse_17(self):
        self.assertEqual(
            PAR.parse(('tag# 1089; bag# 156; no gonads')),
            [ParsedTrait(value='no gonads', flags={'ambiguous_sex': True},
                         start=21, end=30)])

    def test_parse_18(self):
        self.assertEqual(
            PAR.parse(
                'weight=36 g; reproductive data=testes: 11x7 mm (scrotal)'),
            [ParsedTrait(value='scrotal', start=13, end=55)])

    def test_parse_19(self):
        self.assertEqual(
            PAR.parse(
                ('non-scrotal, sem. ves. 14 mm ')),
            [ParsedTrait(value='non scrotal', start=0, end=11)])

    def test_parse_20(self):
        self.assertEqual(
            PAR.parse(
                ('verbatim preservation date=8 October 1986 ; '
                 'reproductive data=No testicles')),
            [ParsedTrait(value='no testicles', start=44, end=74)])

    def test_parse_21(self):
        self.assertEqual(
            PAR.parse(
                ('weight=53 g; reproductive data=testes decended, T=8x3 ;')),
            [ParsedTrait(value='decended', start=13, end=46)])

    def test_parse_22(self):
        self.assertEqual(
            PAR.parse(
                ('weight=75.6 g; reproductive data=Testes small')),
            [ParsedTrait(value='small', start=15, end=45)])

    def test_parse_23(self):
        self.assertEqual(
            PAR.parse(
                ('weight=75.6 g; reproductive data=small')),
            [])

    def test_parse_24(self):
        self.assertEqual(
            PAR.parse('puncture wound in left abdominal region.'),
            [])

    def test_parse_25(self):
        self.assertEqual(
            PAR.parse(' reproductive data=plsc'),
            [])

    def test_parse_26(self):
        self.assertEqual(
            PAR.parse(
                ('junk before reproductive data=Testes small, not descended')),
            [ParsedTrait(value='small not descended', start=12, end=57)])

    def test_parse_27(self):
        self.assertEqual(
            PAR.parse('Mixed woods // TESTES NOT DESCENDED'),
            [ParsedTrait(value='not descended', start=15, end=35)])

    def test_parse_28(self):
        self.assertEqual(
            PAR.parse(
                ('reproductive data=Uteri small, clear')),
            [])
