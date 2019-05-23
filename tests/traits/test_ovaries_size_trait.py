# import unittest
# from traiter.parse import Parse
# from traiter.traits.ovaries_size_trait import OvariesSizeTrait
#
#
# PAR = None
#
#
# class TestOvariesSizeTrait(unittest.TestCase):
#
#     @classmethod
#     def setup_class(cls):
#         global PAR
#         PAR = OvariesSizeTrait()
#
#     def test_parse_01(self):
#         self.assertEqual(
#             PAR.parse('testes = 8x5 mm'),
#             [Parse(value=[8, 5], units='mm', start=0, end=15)])
