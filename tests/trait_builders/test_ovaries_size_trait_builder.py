import unittest
from traiter.numeric_trait import NumericTrait
from traiter.trait_builders.ovaries_size_trait_builder \
    import OvariesSizeTraitBuilder


PAR = None


class TestOvariesSizeTraitBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global PAR
        PAR = OvariesSizeTraitBuilder()

    def test_parse_01(self):
        self.maxDiff = None
        self.assertEqual(
            PAR.parse('ovaries = 8x5 mm'),
            [NumericTrait(value=[8, 5], units='mm', start=0, end=16)])
