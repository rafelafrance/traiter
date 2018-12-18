# pylint: disable=missing-docstring,import-error,too-many-public-methods

from argparse import Namespace
import unittest
from lib.trait_parsers.testes_state import ParseTestesState


class TestTestesStateParser(unittest.TestCase):

    def test_parse_01(self):
        self.assertDictEqual(
            TARGET.parse(['testes descended']),
            {'regex': 'testes_state',
             'key': 'testes',
             'field': 'col1',
             'start': 0,
             'end': 16,
             'value': 'descended'})

    def test_parse_02(self):
        self.assertDictEqual(
            TARGET.parse(['testes undescended']),
            {'regex': 'testes_state',
             'key': 'testes',
             'field': 'col1',
             'start': 0,
             'end': 18,
             'value': 'undescended'})

    def test_parse_03(self):
        self.assertDictEqual(
            TARGET.parse(['testes undesc.']),
            {'regex': 'testes_state',
             'key': 'testes',
             'field': 'col1',
             'start': 0,
             'end': 13,
             'value': 'undesc'})

    def test_parse_04(self):
        self.assertDictEqual(
            TARGET.parse(['testes undesc']),
            {'regex': 'testes_state',
             'key': 'testes',
             'field': 'col1',
             'start': 0,
             'end': 13,
             'value': 'undesc'})

    def test_parse_05(self):
        self.assertDictEqual(
            TARGET.parse(['testes not fully descended']),
            {'regex': 'testes_state',
             'key': 'testes',
             'field': 'col1',
             'start': 0,
             'end': 26,
             'value': 'not fully descended'})

    def test_parse_06(self):
        self.assertDictEqual(
            TARGET.parse(['testes not-scrotal']),
            {'regex': 'testes_state',
             'key': 'testes',
             'field': 'col1',
             'start': 0,
             'end': 18,
             'value': 'not-scrotal'})

    def test_parse_07(self):
        self.assertDictEqual(
            TARGET.parse(['testes no scrotum']),
            {'regex': 'testes_state',
             'key': 'testes',
             'field': 'col1',
             'start': 0,
             'end': 17,
             'value': 'no scrotum'})

    def test_parse_08(self):
        self.assertDictEqual(
            TARGET.parse(['testes nscr']),
            {'regex': 'testes_state',
             'key': 'testes',
             'field': 'col1',
             'start': 0,
             'end': 11,
             'value': 'nscr'})

    def test_parse_09(self):
        self.assertDictEqual(
            TARGET.parse(['testes ns']),
            {'regex': 'testes_state',
             'key': 'testes',
             'field': 'col1',
             'start': 0,
             'end': 9,
             'value': 'ns'})

    def test_parse_10(self):
        self.assertDictEqual(
            TARGET.parse(['tes undescend.']),
            {'regex': 'testes_abbrev_state',
             'key': 'tes',
             'field': 'col1',
             'start': 0,
             'end': 13,
             'value': 'undescend'})

    def test_parse_11(self):
        self.assertDictEqual(
            TARGET.parse(['t abdominal']),
            {'regex': 'testes_abbrev_state',
             'key': 't',
             'field': 'col1',
             'start': 0,
             'end': 11,
             'value': 'abdominal'})

    def test_parse_12(self):
        self.assertDictEqual(
            TARGET.parse(['t nscr']),
            {'regex': 'testes_abbrev_state',
             'key': 't',
             'field': 'col1',
             'start': 0,
             'end': 6,
             'value': 'nscr'})

    def test_parse_13(self):
        self.assertEqual(TARGET.parse('t ns'), None)

    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################

    def test_preferred_or_search_01(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                [('sex=male ; total length=245 mm; tail length=90 mm; '
                  'hind foot with claw=35 mm; '
                  'reproductive data=Testes partially descended. '
                  'Sperm present.')]),
            {'value': 'partially descended',
             'key': 'reproductive data',
             'field': 'col1',
             'start': 78,
             'end': 122,
             'regex': 'reproductive_data',
             'found': True})

    def test_preferred_or_search_02(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                [('sex=male ; reproductive data=testis 5mm, abdominal '
                  '; ear from notch=20 mm; ')]),
            {'value': 'abdominal',
             'key': 'reproductive data',
             'field': 'col1',
             'start': 11,
             'end': 50,
             'regex': 'reproductive_data_keyed',
             'found': True})

    def test_preferred_or_search_03(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                [('tag# 1089; bag# 156; no gonads')]),
            {'value': 'no gonads',
             'key': None,
             'field': 'col1',
             'start': 21,
             'end': 30,
             'regex': 'testes_state_only',
             'found': True})

    def test_preferred_or_search_04(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                ['weight=36 g; reproductive data=testes: 11x7 mm (scrotal)']),
            {'value': 'scrotal',
             'key': 'reproductive data',
             'field': 'col1',
             'start': 13,
             'end': 55,
             'regex': 'reproductive_data',
             'found': True})

    def test_preferred_or_search_05(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                [('"ear length":"15.0", "gonad length 1":"7.0", '
                  '"gonad length 2":"3.0", "hind foot length":"31.0", '
                  '"tail length":"102.0", "total length":"204.0", '
                  '"weight":"48.9" }	non-scrotal, sem. ves. 14 mm, '
                  'little fat')]),
            {'value': 'non-scrotal',
             'key': None,
             'field': 'col1',
             'start': 161,
             'end': 172,
             'regex': 'testes_state_only',
             'found': True})

    def test_preferred_or_search_06(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                [('verbatim preservation date=8 October 1986 ; '
                  'reproductive data=No testicles')]),
            {'value': 'No testicles',
             'key': 'reproductive data',
             'field': 'col1',
             'start': 44,
             'end': 74,
             'regex': 'reproductive_data',
             'found': True})

    def test_preferred_or_search_07(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                [('weight=53 g; reproductive data=testes decended, T=8x3 ;')]),
            {'value': 'decended',
             'key': 'reproductive data',
             'field': 'col1',
             'start': 13,
             'end': 46,
             'regex': 'reproductive_data',
             'found': True})

    def test_preferred_or_search_08(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                [('weight=75.6 g; reproductive data=Testes small')]),
            {'value': 'small',
             'key': 'reproductive data',
             'field': 'col1',
             'start': 15,
             'end': 45,
             'regex': 'reproductive_data_keyed',
             'found': True})

    def test_preferred_or_search_09(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                [('weight=75.6 g; reproductive data=small')]),
            {'value': 'small',
             'key': 'reproductive data',
             'field': 'col1',
             'start': 15,
             'end': 38,
             'regex': 'reproductive_data_immediate',
             'found': True})

    def test_preferred_or_search_10(self):
        # Make sure we don't pick up a stray 'abdonminal'
        self.assertDictEqual(
            TARGET.keyword_search(
                [('reproductive data=unknown '
                  'No ecto/endoparasites found. Part of the tail was missing, '
                  'puncture wound in left abdominal region.')]),
            {'value': None,
             'key': None,
             'field': None,
             'start': None,
             'end': None,
             'regex': None,
             'found': False})

    def test_preferred_or_search_11(self):
        self.assertDictEqual(
            TARGET.keyword_search([(' reproductive data=plsc')]),
            {'value': None,
             'key': None,
             'field': None,
             'start': None,
             'end': None,
             'regex': None,
             'found': False})

    def test_preferred_or_search_12(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                ['junk before reproductive data=Testes small, not descended']),
            {'value': 'small, not descended',
             'key': 'reproductive data',
             'field': 'col1',
             'start': 12,
             'end': 57,
             'regex': 'reproductive_data',
             'found': True})

    def test_preferred_or_search_13(self):
        self.assertDictEqual(
            TARGET.keyword_search(['Mixed woods // TESTES NOT DESCENDED']),
            {'value': 'NOT DESCENDED',
             'key': 'TESTES',
             'field': 'col1',
             'start': 15,
             'end': 35,
             'regex': 'testes_state',
             'found': True})

    def test_preferred_or_search_14(self):
        self.assertDictEqual(
            TARGET.keyword_search(['reproductive data=Uteri small, clear']),
            {'value': None,
             'key': None,
             'field': None,
             'start': None,
             'end': None,
             'regex': None,
             'found': False})


ARGS = Namespace(columns=['col1', 'col2', 'col3'])
TARGET = ParseTestesState(ARGS)
SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(TestTestesStateParser)
unittest.TextTestRunner().run(SUITE)
