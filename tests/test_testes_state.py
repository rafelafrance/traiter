# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.trait_parsers.testes_state import ParseTestesState


class TestTestesStateParser(unittest.TestCase):

    def test_parse_01(self):
        self.assertDictEqual(
            TARGET.parse('testes descended'),
            {'regex': 'testes_state',
             'key': 'testes',
             'value': 'descended'})

    def test_parse_02(self):
        self.assertDictEqual(
            TARGET.parse('testes undescended'),
            {'regex': 'testes_state',
             'key': 'testes',
             'value': 'undescended'})

    def test_parse_03(self):
        self.assertDictEqual(
            TARGET.parse('testes undesc.'),
            {'regex': 'testes_state',
             'key': 'testes',
             'value': 'undesc.'})

    def test_parse_04(self):
        self.assertDictEqual(
            TARGET.parse('testes undesc'),
            {'regex': 'testes_state',
             'key': 'testes',
             'value': 'undesc'})

    def test_parse_05(self):
        self.assertDictEqual(
            TARGET.parse('testes not fully descended'),
            {'regex': 'testes_state',
             'key': 'testes',
             'value': 'not fully descended'})

    def test_parse_06(self):
        self.assertDictEqual(
            TARGET.parse('testes not-scrotal'),
            {'regex': 'testes_state',
             'key': 'testes',
             'value': 'not-scrotal'})

    def test_parse_07(self):
        self.assertDictEqual(
            TARGET.parse('testes no scrotum'),
            {'regex': 'testes_state',
             'key': 'testes',
             'value': 'no scrotum'})

    def test_parse_08(self):
        self.assertDictEqual(
            TARGET.parse('testes nscr'),
            {'regex': 'testes_state',
             'key': 'testes',
             'value': 'nscr'})

    def test_parse_09(self):
        self.assertDictEqual(
            TARGET.parse('testes ns'),
            {'regex': 'testes_state',
             'key': 'testes',
             'value': 'ns'})

    def test_parse_10(self):
        self.assertDictEqual(
            TARGET.parse('tes undescend.'),
            {'regex': 'testes_abbrev_state',
             'key': 'tes',
             'value': 'undescend.'})

    def test_parse_11(self):
        self.assertDictEqual(
            TARGET.parse('t abdominal'),
            {'regex': 'testes_abbrev_state',
             'key': 't',
             'value': 'abdominal'})

    def test_parse_12(self):
        self.assertDictEqual(
            TARGET.parse('t nscr'),
            {'regex': 'testes_abbrev_state',
             'key': 't',
             'value': 'nscr'})

    def test_parse_13(self):
        self.assertEqual(TARGET.parse('t ns'), None)


TARGET = ParseTestesState()
SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(TestTestesStateParser)
unittest.TextTestRunner().run(SUITE)
