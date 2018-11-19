# pylint: disable=missing-docstring,import-error,too-many-public-methods

from argparse import Namespace
import unittest
from lib.trait_parsers.sex import ParseSex


class TestSexParser(unittest.TestCase):

    def test_sex_key_value_delimited_01(self):
        self.assertDictEqual(
            TARGET.parse(['weight=81.00 g; sex=female ? ; age=u ad.']),
            {'key': 'sex',
             'field': 'col1',
             'start': 16,
             'end': 30,
             'value': 'female ?',
             'regex': 'sex_key_value_delimited'})

    def test_sex_key_value_delimited_02(self):
        self.assertDictEqual(
            TARGET.parse(['sex=unknown ; crown-rump length=8 mm']),
            {'key': 'sex',
             'field': 'col1',
             'start': 0,
             'end': 13,
             'value': 'unknown',
             'regex': 'sex_key_value_delimited'})

    def test_sex_key_value_undelimited_01(self):
        self.assertDictEqual(
            TARGET.parse(['sex=F crown rump length=8 mm']),
            {'key': 'sex',
             'field': 'col1',
             'start': 0,
             'end': 5,
             'value': 'F',
             'regex': 'sex_key_value_undelimited'})

    def test_sex_unkeyed_01(self):
        self.assertDictEqual(
            TARGET.parse(['words male female unknown more words']),
            {'key': None,
             'field': 'col1',
             'start': [6, 11],
             'end': [10, 17],
             'value': ['male', 'female'],
             'regex': 'sex_unkeyed'})

    def test_sex_unkeyed_02(self):
        self.assertEqual(
            TARGET.parse(['words male female male more words']),
            None)

    def test_excluded_01(self):
        self.assertEqual(
            TARGET.parse(['Respective sex and msmt. in mm']),
            None)

    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################

    def test_preferred_or_search_01(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                ['weight=81.00 g; sex=female ? ; age=u ad.']),
            {'key': 'sex',
             'regex': 'sex_key_value_delimited',
             'field': 'col1',
             'start': 16,
             'end': 30,
             'value': 'female ?',
             'found': True})

    def test_preferred_or_search_02(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                ['sex=unknown ; crown-rump length=8 mm']),
            {'value': 'unknown',
             'key': 'sex',
             'regex': 'sex_key_value_delimited',
             'field': 'col1',
             'start': 0,
             'end': 13,
             'found': True})

    def test_preferred_or_search_03(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                ['sex=F crown rump length=8 mm']),
            {'value': 'F',
             'key': 'sex',
             'regex': 'sex_key_value_undelimited',
             'field': 'col1',
             'start': 0,
             'end': 5,
             'found': True})

    def test_preferred_or_search_04(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                ['words male female unknown more words']),
            {'value': 'male,female',
             'key': None,
             'regex': 'sex_unkeyed',
             'field': 'col1',
             'start': [6, 11],
             'end': [10, 17],
             'found': True})

    def test_preferred_or_search_05(self):
        self.assertEqual(
            TARGET.keyword_search(['words male female male more words']),
            {'value': '',
             'key': None,
             'regex': None,
             'field': None,
             'start': None,
             'end': None,
             'found': False})

    def test_preferred_or_search_06(self):
        self.assertEqual(
            TARGET.keyword_search(['Respective sex and msmt. in mm']),
            {'value': '',
             'key': None,
             'regex': None,
             'field': None,
             'start': None,
             'end': None,
             'found': False})

    def test_preferred_or_search_07(self):
        self.assertEqual(
            TARGET.keyword_search(['mention male in a phrase']),
            {'value': 'male',
             'key': None,
             'regex': 'sex_unkeyed',
             'field': 'col1',
             'start': 8,
             'end': 12,
             'found': True})

    def test_preferred_or_search_08(self):
        self.assertEqual(
            TARGET.keyword_search(['male in a phrase']),
            {'value': 'male',
             'key': None,
             'regex': 'sex_unkeyed',
             'field': 'col1',
             'start': 0,
             'end': 4,
             'found': True})

    def test_preferred_or_search_09(self):
        self.assertEqual(
            TARGET.keyword_search(['male or female']),
            {'value': 'male,female',
             'key': None,
             'regex': 'sex_unkeyed',
             'field': 'col1',
             'start': [0, 8],
             'end': [4, 14],
             'found': True})


ARGS = Namespace(columns=['col1', 'col2', 'col3'])
TARGET = ParseSex(ARGS)
SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(TestSexParser)
unittest.TextTestRunner().run(SUITE)
