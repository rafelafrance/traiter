import unittest
from lib.numeric_trait import NumericTrait
from lib.trait_builders.embryo_count_trait_builder \
    import EmbryoCountTraitBuilder


PAR = None


class TestEmbryoCountTraitBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global PAR
        PAR = EmbryoCountTraitBuilder()

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('pregnant; 4 emb'),
            [NumericTrait(value=4, start=10, end=15)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('not pregnant; no embs'),
            [NumericTrait(value=0, start=14, end=21)])

    # def test_parse_03(self):
    #     self.maxDiff = None
    #     self.assertEqual(
    #         PAR.parse('pregnant; 4 emb 3L 1R'),
    #         [NumericTrait(value=4, start=14, end=21),
    #          NumericTrait(value=3, side='L', start=14, end=21),
    #          NumericTrait(value=1, side='R', start=14, end=21)])
