# import unittest
#
# from tests.setup import test
#
#
# class TestElevationPatterns(unittest.TestCase):
#
#     def test_elevation_01(self):
#         self.assertEqual(
#             test("""Alt.: 1463m/4800ft."""),
#             [
#                 {
#                     "altitude": 1463.0,
#                     "trait": "altitude",
#                     "units": "meters",
#                     "start": 0,
#                     "end": 11,
#                 },
#             ],
#         )
