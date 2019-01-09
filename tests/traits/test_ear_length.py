# flake8=noqa

import unittest
from lib.parse_result import ParseResult
from lib.traits.ear_length import EarLength


PAR = EarLength()


class TestEarLength(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('earLengthInmm: 9'),
            [ParseResult(value=9, units='earlengthinmm', start=0, end=16)])

    def test_parse_02(self):
        self.assertEqual(
            #          0123456789 123456789 123456789 123456789 123456789
            PAR.parse('L. 9", T. 4", ear 9/16"'),
            [ParseResult(value=14.29, units='"', start=14, end=23)])
