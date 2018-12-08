# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.parsers.sex_parser import SexParser


PR = SexParser()


class TestSexParser(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            #         0123456789.123456789.123456789.123456789.123456789.123456
            PR.parse('sex=female ?'),
            [{'value': 'female ?', 'start': 0, 'end': 12}])

    def test_parse_02(self):
        self.assertEqual(
            #         0123456789.123456789.123456789.123456789.123456789.123456
            PR.parse('sex=unknown ; crown-rump length=8 mm'),
            [{'value': 'unknown', 'start': 0, 'end': 11}])

    def test_parse_03(self):
        self.assertEqual(
            #         0123456789.123456789.123456789.123456789.123456789.123456
            PR.parse('sex=F crown rump length=8 mm'),
            [{'value': 'F', 'start': 0, 'end': 5}])

    def test_parse_04(self):
        self.assertEqual(
            #         0123456789.123456789.123456789.123456789.123456789.123456
            PR.parse('words male female unknown more words'),
            [{'value': 'male', 'start': 6, 'end': 10},
             {'value': 'female', 'start': 11, 'end': 17}])

    def test_parse_05(self):
        self.assertEqual(
            #         0123456789.123456789.123456789.123456789.123456789.123456
            PR.parse('words male female male more words'),
            [])

    def test_parse_06(self):
        self.assertEqual(
            #         0123456789.123456789.123456789.123456789.123456789.123456
            PR.parse('Respective sex and msmt. in mm'),
            [])

    def test_parse_07(self):
        self.assertEqual(
            #         0123456789.123456789.123456789.123456789.123456789.123456
            PR.parse('male or female'),
            [{'value': 'male', 'start': 0, 'end': 4},
             {'value': 'female', 'start': 8, 'end': 14}])

    def test_parse_08(self):
        self.assertEqual(
            #         0123456789.123456789.123456789.123456789.123456789.123456
            PR.parse('sex=unknown length=8 mm'),
            [{'value': 'unknown', 'start': 0, 'end': 11}])
