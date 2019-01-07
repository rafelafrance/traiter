# flake8=noqa

import unittest
from lib.base import Result
from lib.traits.as_is import AsIs


PAR = AsIs()


class TestAsIs(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('word'),
            [Result(value='word', start=0, end=4)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse(' word  '),
            [Result(value='word', start=1, end=5)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse(' x  '),
            [Result(value='x', start=1, end=2)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('x'),
            [Result(value='x', start=0, end=1)])

    def test_parse_05(self):
        self.assertEqual(PAR.parse(''), [])

    def test_parse_06(self):
        self.assertEqual(PAR.parse('  '), [])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse(' word  word '),
            [Result(value='word  word', start=1, end=11)])
