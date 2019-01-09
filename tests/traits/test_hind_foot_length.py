# flake8=noqa

import unittest
from lib.parse_result import ParseResult
from lib.traits.hind_foot_length import HindFootLength


PAR = HindFootLength()


# class TestHindFootLength(unittest.TestCase):
#
#     def test_parse_01(self):
#         self.assertEqual(
#             PAR.parse('tailLengthInmm: 102'),
#             [ParseResult(value=102.0, units='taillengthinmm', start=0, end=19)])
