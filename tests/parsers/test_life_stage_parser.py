# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.parsers.life_stage_parser import LifeStageParser


PAR = LifeStageParser()


class TestLifeStageParser(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('sex=unknown ; age class=adult/juvenile'),
            [{'value': 'adult/juvenile', 'start': 14, 'end': 38}])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('age=u ad.'),
            [{'value': 'u ad', 'start': 0, 'end': 9}])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse(
                'weight=5.2 g; age class=over-winter ; total length=99 mm;0'),
            [{'value': 'over-winter', 'start': 14, 'end': 37}])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse(
                'sex=female ? ; age=1st year more than four words here'),
            [{'value': '1st year', 'start': 15, 'end': 27}])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('words after hatching year more words'),
            [{'value': 'after hatching year', 'start': 6, 'end': 25}])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('age determined by 20-sided die'),
            [])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('LifeStage Remarks: 5-6 wks'),
            [{'value': '5-6 wks', 'start': 0, 'end': 26}])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('mentions juvenile'),
            [{'value': 'juvenile', 'start': 9, 'end': 17}])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('mentions juveniles in the field'),
            [{'value': 'juveniles', 'start': 9, 'end': 18}])
