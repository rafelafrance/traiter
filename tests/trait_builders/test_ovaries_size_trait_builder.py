# import unittest
# from traiter.parse import Parse
# from traiter.trait_builders.ovaries_size_trait import OvariesSizeTrait
#
#
# PAR = None
#
#
# class TestOvariesSizeTraitBuilder(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         global PAR
#         PAR = OvariesSizeTraitBuilder()
#
#     def test_parse_01(self):
#         self.assertEqual(
#             PAR.parse('testes = 8x5 mm'),
#             [Parse(value=[8, 5], units='mm', start=0, end=15)])


# if __name__ == '__main__':
#     unittest.main()
