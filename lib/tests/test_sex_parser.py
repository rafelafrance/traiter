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


target = SexParser()
suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSexParser)
unittest.TextTestRunner().run(suite)
