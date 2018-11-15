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
             'end': 14,
             'value': 'undesc.'})

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
             'end': 14,
             'value': 'undescend.'})

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


ARGS = Namespace(columns=['col1', 'col2', 'col3'])
TARGET = ParseTestesState(ARGS)
SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(TestTestesStateParser)
unittest.TextTestRunner().run(SUITE)
