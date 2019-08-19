import unittest
from lib.trait import Trait
from lib.trait_builders.lactation_state_trait_builder \
    import LactationStateTraitBuilder


PAR = None


class TestSexTraitBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global PAR
        PAR = LactationStateTraitBuilder()

    # def test_parse_01(self):
    #     self.assertEqual(
    #         PAR.parse('sex=female ?'),
    #         [Trait(value='female ?', start=0, end=12)])
