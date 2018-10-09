import unittest
from trait_parsers.sex_parser import SexParser


class TestSexParser(unittest.TestCase):

    def test_sex_key_value_delimited_1(self):
        self.assertDictEqual(
            target.parse('weight=81.00 g; sex=female ? ; age=u ad.'),
            {'key': 'sex', 'value': 'female ?'})

    def test_sex_key_value_delimited_2(self):
        self.assertDictEqual(
            target.parse('sex=unknown ; crown-rump length=8 mm'),
            {'key': 'sex', 'value': 'unknown'})

    def test_sex_key_value_undelimited_1(self):
        self.assertDictEqual(
            target.parse('sex=F crown rump length=8 mm'),
            {'key': 'sex', 'value': 'F'})

    def test_sex_unkeyed_1(self):
        self.assertDictEqual(
            target.parse('words male female unknown more words'),
            {'key': None, 'value': ['male', 'female']})

    def test_sex_unkeyed_2(self):
        self.assertEqual(
            target.parse('words male female male more words'),
            None)

    def test_excluded_1(self):
        self.assertEqual(
            target.parse('Respective sex and msmt. in mm'),
            None)

    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################

    def test_preferred_or_search_1(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['weight=81.00 g; sex=female ? ; age=u ad.']),
            {'derivedsex': 'female ?', 'hassex': 1})

    def test_preferred_or_search_2(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['sex=unknown ; crown-rump length=8 mm']),
            {'derivedsex': 'unknown', 'hassex': 1})

    def test_preferred_or_search_3(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['sex=F crown rump length=8 mm']),
            {'derivedsex': 'F', 'hassex': 1})

    def test_preferred_or_search_4(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['words male female unknown more words']),
            {'derivedsex': 'male,female', 'hassex': 1})

    def test_preferred_or_search_5(self):
        self.assertEqual(
            target.preferred_or_search('', ['words male female male more words']),
            {'derivedsex': '', 'hassex': 0})

    def test_preferred_or_search_6(self):
        self.assertEqual(
            target.preferred_or_search('', ['Respective sex and msmt. in mm']),
            {'derivedsex': '', 'hassex': 0})

    def test_preferred_or_search_7(self):
        self.assertEqual(
            target.preferred_or_search('', ['mention male in a phrase']),
            {'derivedsex': 'male', 'hassex': 1})

    def test_preferred_or_search_8(self):
        self.assertEqual(
            target.preferred_or_search('', ['male in a phrase']),
            {'derivedsex': 'male', 'hassex': 1})

    def test_preferred_or_search_9(self):
        self.assertEqual(
            target.preferred_or_search('', ['male or female']),
            {'derivedsex': 'male,female', 'hassex': 1})


target = SexParser()
suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSexParser)
unittest.TextTestRunner().run(suite)
