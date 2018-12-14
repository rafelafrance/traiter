# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.parsers.life_stage import ParseLifeStage


PAR = ParseLifeStage()


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

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('one or more adults'),
            [{'value': 'adults', 'start': 12, 'end': 18}])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('adults'),
            [{'value': 'adults', 'start': 0, 'end': 6}])

    def test_parse_12(self):
        self.assertEqual(
            PAR.parse('Adulte'),
            [{'value': 'Adulte', 'start': 0, 'end': 6}])

    def test_parse_13(self):
        self.assertEqual(
            PAR.parse('AGE IMM'),
            [{'value': 'IMM', 'start': 0, 'end': 7}])

    def test_parse_14(self):
        self.assertEqual(
            PAR.parse('subadult'),
            [{'value': 'subadult', 'start': 0, 'end': 8}])

    def test_parse_15(self):
        self.assertEqual(
            PAR.parse('subadultery'),
            [])

    def test_parse_16(self):
        self.assertEqual(
            PAR.parse('in which larvae are found'),
            [{'value': 'larvae', 'start': 9, 'end': 15}])

    def test_parse_17(self):
        self.assertEqual(
            PAR.parse('one tadpole'),
            [{'value': 'tadpole', 'start': 4, 'end': 11}])

    def test_parse_18(self):
        # Lifestage removed
        self.assertEqual(
            PAR.parse('some embryos'),
            [])

    def test_parse_19(self):
        self.assertEqual(
            PAR.parse('young adult'),
            [{'value': 'young adult', 'start': 0, 'end': 11}])

    def test_parse_20(self):
        self.assertEqual(
            PAR.parse('adult young'),
            [{'value': 'adult', 'start': 0, 'end': 5},
             {'value': 'young', 'start': 6, 'end': 11}])

    def test_parse_21(self):
        self.assertEqual(
            PAR.parse('sub-adult'),
            [{'value': 'sub-adult', 'start': 0, 'end': 9}])

    def test_parse_22(self):
        self.assertEqual(
            PAR.parse('adult(s) and juvenile(s)'),
            [{'value': 'adult', 'start': 0, 'end': 5},
             {'value': 'juvenile', 'start': 13, 'end': 21}])

    def test_parse_23(self):
        self.assertEqual(
            PAR.parse('young-of-the-year'),
            [{'value': 'young-of-the-year', 'start': 0, 'end': 17}])

    def test_parse_24(self):
        self.assertEqual(
            PAR.parse('YOLK SAC'),
            [{'value': 'YOLK SAC', 'start': 0, 'end': 8}])
