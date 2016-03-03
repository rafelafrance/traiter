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


target = LifeStageParser()
suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestLifeStageParser)
unittest.TextTestRunner().run(suite)
