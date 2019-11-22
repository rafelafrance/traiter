# import unittest
# from pylib.efloras.trait import Trait
# from pylib.efloras.parsers.plant_count import SEPAL_COUNT
#
#
# class TestFlowerShape(unittest.TestCase):
#
#     def test_parse_01(self):
#         self.assertEqual(
#             SEPAL_COUNT.parse('Sepals 1-4,'),
#             [Trait(start=0, end=10, part='sepals', low=1, high=4)])
#
#     def test_parse_02(self):
#         self.assertEqual(
#             SEPAL_COUNT.parse('Sepals 1-4 mm;'),
#             [])
#
#     def test_parse_03(self):
#         self.assertEqual(
#             SEPAL_COUNT.parse('Sepals up to 4,'),
#             [Trait(start=0, end=14, part='sepals', high=4)])
#
#     def test_parse_04(self):
#         self.assertEqual(
#             SEPAL_COUNT.parse('Sepals up to 4 mm;'),
#             [])
#
#     def test_parse_05(self):
#         self.assertEqual(
#             SEPAL_COUNT.parse(
#                 'sepals 6, incurved at apex, red-tipped, equal, 1-1.5 mm'),
#             [Trait(start=0, end=8, part='sepals', low=6)])
