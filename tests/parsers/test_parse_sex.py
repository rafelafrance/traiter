# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.parsers.shared_reducers import Result
from lib.parsers.parse_sex import ParseSex


PAR = ParseSex()


class TestParseSex(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('sex=female ?'),
            [Result(value='female ?', start=0, end=12)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('sex=unknown ; crown-rump length=8 mm'),
            [Result(value='unknown', start=0, end=11)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('sex=F crown rump length=8 mm'),
            [Result(value='F', start=0, end=5)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('words male female unknown more words'),
            [Result(value='male', start=6, end=10),
             Result(value='female', start=11, end=17)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('words male female male more words'),
            [Result(value='male', start=6, end=10),
             Result(value='female', start=11, end=17),
             Result(value='male', start=18, end=22)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('Respective sex and msmt. in mm'),
            [])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('male or female'),
            [Result(value='male', start=0, end=4),
             Result(value='female', start=8, end=14)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('sex=unknown length=8 mm'),
            [Result(value='unknown', start=0, end=11)])

    def test_post_process_01(self):
        results = [Result(value='male', start=6, end=10),
                   Result(value='female', start=11, end=17)]
        self.assertEqual(PAR.post_process(results), results)

    def test_post_process_02(self):
        results = [Result(value='male', start=6, end=10),
                   Result(value='female', start=11, end=17),
                   Result(value='male', start=18, end=22)]
        self.assertEqual(PAR.post_process(results), [])
