# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.trait_parsers.sex import SexParser


class TestSexParser(unittest.TestCase):

    def test_sex_key_value_delimited_01(self):
        self.assertDictEqual(
            TARGET.parse('weight=81.00 g; sex=female ? ; age=u ad.'),
            {'key': 'sex',
             'value': 'female ?',
             'regex': 'sex_key_value_delimited'})

    def test_sex_key_value_delimited_02(self):
        self.assertDictEqual(
            TARGET.parse('sex=unknown ; crown-rump length=8 mm'),
            {'key': 'sex',
             'value': 'unknown',
             'regex': 'sex_key_value_delimited'})

    def test_sex_key_value_undelimited_01(self):
        self.assertDictEqual(
            TARGET.parse('sex=F crown rump length=8 mm'),
            {'key': 'sex',
             'value': 'F',
             'regex': 'sex_key_value_undelimited'})

    def test_sex_unkeyed_01(self):
        self.assertDictEqual(
            TARGET.parse('words male female unknown more words'),
            {'key': None,
             'value': ['male', 'female'],
             'regex': 'sex_unkeyed'})

    def test_sex_unkeyed_02(self):
        self.assertEqual(
            TARGET.parse('words male female male more words'),
            None)

    def test_excluded_01(self):
        self.assertEqual(
            TARGET.parse('Respective sex and msmt. in mm'),
            None)

    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################

    def test_preferred_or_search_01(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(
                '', ['weight=81.00 g; sex=female ? ; age=u ad.']),
            {'key': 'sex',
             'regex': 'sex_key_value_delimited',
             'derived_sex': 'female ?',
             'has_sex': True})

    def test_preferred_or_search_02(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(
                '', ['sex=unknown ; crown-rump length=8 mm']),
            {'derived_sex': 'unknown',
             'key': 'sex',
             'regex': 'sex_key_value_delimited',
             'has_sex': True})

    def test_preferred_or_search_03(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(
                '', ['sex=F crown rump length=8 mm']),
            {'derived_sex': 'F',
             'key': 'sex',
             'regex': 'sex_key_value_undelimited',
             'has_sex': True})

    def test_preferred_or_search_04(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(
                '', ['words male female unknown more words']),
            {'derived_sex': 'male,female',
             'key': None,
             'regex': 'sex_unkeyed',
             'has_sex': True})

    def test_preferred_or_search_05(self):
        self.assertEqual(
            TARGET.preferred_or_search(
                '', ['words male female male more words']),
            {'derived_sex': '',
             'key': None,
             'regex': None,
             'has_sex': False})

    def test_preferred_or_search_06(self):
        self.assertEqual(
            TARGET.preferred_or_search(
                '', ['Respective sex and msmt. in mm']),
            {'derived_sex': '',
             'key': None,
             'regex': None,
             'has_sex': False})

    def test_preferred_or_search_07(self):
        self.assertEqual(
            TARGET.preferred_or_search('', ['mention male in a phrase']),
            {'derived_sex': 'male',
             'key': None,
             'regex': 'sex_unkeyed',
             'has_sex': True})

    def test_preferred_or_search_08(self):
        self.assertEqual(
            TARGET.preferred_or_search('', ['male in a phrase']),
            {'derived_sex': 'male',
             'key': None,
             'regex': 'sex_unkeyed',
             'has_sex': True})

    def test_preferred_or_search_09(self):
        self.assertEqual(
            TARGET.preferred_or_search('', ['male or female']),
            {'derived_sex': 'male,female',
             'key': None,
             'regex': 'sex_unkeyed',
             'has_sex': True})


TARGET = SexParser()
SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(TestSexParser)
unittest.TextTestRunner().run(SUITE)
