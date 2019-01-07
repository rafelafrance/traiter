# flake8=noqa

import unittest
from lib.base import Result
from lib.traits.tail_length import TailLength


PAR = TailLength()


# class TestTailLength(unittest.TestCase):
#
#     def test_parse_01(self):
#         self.assertEqual(
#             PAR.parse('{"totalLengthInMM":"123" };'),
#             [Result(value=123.0, units='mm', start=2, end=23)])
