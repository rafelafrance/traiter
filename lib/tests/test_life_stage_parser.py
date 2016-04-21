import unittest
from trait_parsers.life_stage_parser import LifeStageParser


class TestLifeStageParser(unittest.TestCase):

    def test_life_stage_key_value_delimited_1(self):
        self.assertDictEqual(
            target.parse('sex=unknown ; age class=adult/juvenile'),
            {'key': 'age class', 'value': 'adult/juvenile'})

    def test_life_stage_key_value_delimited_2(self):
        self.assertDictEqual(
            target.parse('weight=81.00 g; sex=female ? ; age=u ad.'),
            {'key': 'age', 'value': 'u ad.'})

    def test_life_stage_key_value_delimited_3(self):
        self.assertDictEqual(
            target.parse('weight=5.2 g; age class=over-winter ; total length=99 mm;'),
            {'key': 'age class', 'value': 'over-winter'})

    def test_life_stage_key_value_undelimited_1(self):
        self.assertDictEqual(
            target.parse('sex=female ? ; age=1st year more than four words here'),
            {'key': 'age', 'value': '1st year'})

    def test_life_stage_no_keyword_1(self):
        self.assertDictEqual(
            target.parse('words after hatching year more words'),
            {'key': None, 'value': 'after hatching year'})

    def test_excluded_1(self):
        self.assertEqual(
            target.parse('age determined by 20-sided die'),
            None)

    def test_life_stage_no_keyword_2(self):
        self.assertDictEqual(
            target.parse('LifeStage Remarks: 5-6 wks'),
            {'key': 'LifeStage Remarks', 'value': '5-6 wks'})

    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################

    def test_preferred_or_search_1(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['sex=unknown ; age class=adult/juvenile']),
            {'derivedLifeStage': 'adult/juvenile', 'hasLifeStage': 1})

    def test_preferred_or_search_2(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['weight=81.00 g; sex=female ? ; age=u ad.']),
            {'derivedLifeStage': 'u ad.', 'hasLifeStage': 1})

    def test_preferred_or_search_3(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['weight=5.2 g; age class=over-winter ; total length=99 mm;']),
            {'derivedLifeStage': 'over-winter', 'hasLifeStage': 1})

    def test_preferred_or_search_4(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['sex=female ? ; age=1st year more than four words here']),
            {'derivedLifeStage': '1st year', 'hasLifeStage': 1})

    def test_preferred_or_search_5(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['words after hatching year more words']),
            {'derivedLifeStage': 'after hatching year', 'hasLifeStage': 1})

    def test_preferred_or_search_6(self):
        self.assertEqual(
            target.preferred_or_search('', ['age determined by 20-sided die']),
            {'derivedLifeStage': '', 'hasLifeStage': 0})

    def test_preferred_or_search_7(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['LifeStage Remarks: 5-6 wks']),
            {'derivedLifeStage': '5-6 wks', 'hasLifeStage': 1})


target = LifeStageParser()
suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestLifeStageParser)
unittest.TextTestRunner().run(suite)
