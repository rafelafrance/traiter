import unittest
from lib.trait import Trait
from lib.trait_builders.placental_scar_location_trait_builder \
    import PlacentalScarLocationTraitBuilder


PAR = None


class TestSexTraitBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global PAR
        PAR = PlacentalScarLocationTraitBuilder()

    # def test_parse_01(self):
    #     self.assertEqual(
    #         PAR.parse('vagina closed, nipples large'),
    #         [Trait(value='nipples large', start=15, end=28)])
