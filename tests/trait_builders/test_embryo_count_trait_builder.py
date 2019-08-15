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

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('pregnant; 4 emb 3L 1R'),
            [NumericTrait(value=4, start=10, end=21),
             NumericTrait(value=3, side='L', start=10, end=21),
             NumericTrait(value=1, side='R', start=10, end=21)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('embryos 2R-1L'),
            [NumericTrait(value=3, start=0, end=13),
             NumericTrait(value=2, side='R', start=0, end=13),
             NumericTrait(value=1, side='L', start=0, end=13)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('embryo of 34402'),
            [])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('138-62-18-6  12.4g  scars  emb.1R,1L; '),
            [NumericTrait(value=2, start=27, end=36),
             NumericTrait(value=1, side='R', start=27, end=36),
             NumericTrait(value=1, side='L', start=27, end=36)])

    def test_parse_07(self):
        self.maxDiff = None
        self.assertEqual(
            PAR.parse('; reproductive data=embryos: 4 right , 2 left  ;'),
            [NumericTrait(value=6, start=20, end=45),
             NumericTrait(value=4, side='right', start=20, end=45),
             NumericTrait(value=2, side='left', start=20, end=45)])
