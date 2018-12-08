# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.parsers.testes_state_parser import ParserTestesState


PAR = ParserTestesState()


class TestParseTestesState(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('some words reproductive data=No testicles; more words'),
            [{'value': 'No testicles', 'start': 11, 'end': 41}])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('testes descended'),
            [{'value': 'descended',
              'start': 0,
              'end': 16}])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('testes undescended'),
            [{'value': 'undescended',
              'start': 0,
              'end': 18}])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('testes undesc.'),
            [{'value': 'undesc',
              'start': 0,
              'end': 13}])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('testes undesc'),
            [{'value': 'undesc',
              'start': 0,
              'end': 13}])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('testes not fully descended'),
            [{'value': 'not fully descended',
              'start': 0,
              'end': 26}])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('testes not-scrotal'),
            [{'value': 'not-scrotal',
              'start': 0,
              'end': 18}])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('testes no scrotum'),
            [{'value': 'no scrotum',
              'start': 0,
              'end': 17}])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('testis nscr'),
            [{'value': 'nscr',
              'start': 0,
              'end': 11}])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('testes ns'),
            [{'value': 'ns',
              'start': 0,
              'end': 9}])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('tes undescend.'),
            [{'value': 'undescend',
              'start': 0,
              'end': 13}])

    def test_parse_12(self):
        self.assertEqual(
            PAR.parse('t abdominal'),
            [{'value': 'abdominal',
              'start': 0,
              'end': 11}])

    def test_parse_13(self):
        self.assertEqual(
            PAR.parse('t nscr'),
            [{'value': 'nscr',
              'start': 0,
              'end': 6}])

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
            [{'value': 'partially descended',
              'start': 27,
              'end': 71}])

    def test_parse_16(self):
        self.assertEqual(
            PAR.parse(
                ('sex=male ; reproductive data=testis 5mm, abdominal '
                 '; ear from notch=20 mm; ')),
            [{'value': 'abdominal',
              'start': 11,
              'end': 50}])

    def test_parse_17(self):
        self.assertEqual(
            PAR.parse(('tag# 1089; bag# 156; no gonads')),
            [{'value': 'no gonads',
              'start': 21,
              'end': 30}])

    def test_parse_18(self):
        self.assertEqual(
            PAR.parse(
                'weight=36 g; reproductive data=testes: 11x7 mm (scrotal)'),
            [{'value': 'scrotal',
              'start': 13,
              'end': 55}])

    def test_parse_19(self):
        self.assertEqual(
            PAR.parse(
                ('"ear length":"15.0", "gonad length 1":"7.0", '
                 '"gonad length 2":"3.0", "hind foot length":"31.0", '
                 '"tail length":"102.0", "total length":"204.0", '
                 '"weight":"48.9" }	non-scrotal, sem. ves. 14 mm, '
                 'little fat')),
            [{'value': 'non-scrotal',
              'start': 161,
              'end': 172}])

    def test_parse_20(self):
        self.assertEqual(
            PAR.parse(
                ('verbatim preservation date=8 October 1986 ; '
                 'reproductive data=No testicles')),
            [{'value': 'No testicles',
              'start': 44,
              'end': 74}])

    def test_parse_21(self):
        self.assertEqual(
            PAR.parse(
                ('weight=53 g; reproductive data=testes decended, T=8x3 ;')),
            [{'value': 'decended',
              'start': 13,
              'end': 46}])

    def test_parse_22(self):
        self.assertEqual(
            PAR.parse(
                ('weight=75.6 g; reproductive data=Testes small')),
            [{'value': 'small',
              'start': 15,
              'end': 45}])

    def test_parse_23(self):
        self.assertEqual(
            PAR.parse(
                ('weight=75.6 g; reproductive data=small')),
            [])

    def test_parse_24(self):
        self.assertEqual(
            PAR.parse(
                ('reproductive data=unknown '
                 'No ecto/endoparasites found. Part of the tail was missing, '
                 'puncture wound in left abdominal region.')),
            [])

    def test_parse_25(self):
        self.assertEqual(
            PAR.parse(' reproductive data=plsc'),
            [])

    def test_parse_26(self):
        self.assertEqual(
            PAR.parse(
                ('junk before reproductive data=Testes small, not descended')),
            [{'value': 'small, not descended',
              'start': 12,
              'end': 57}])

    def test_parse_27(self):
        self.assertEqual(
            PAR.parse('Mixed woods // TESTES NOT DESCENDED'),
            [{'value': 'NOT DESCENDED',
              'start': 15,
              'end': 35}])

    def test_parse_28(self):
        self.assertEqual(
            PAR.parse(
                ('reproductive data=Uteri small, clear')),
            [])
