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
            [NumericTrait(value=4, left=3, right=1, start=10, end=21)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('embryos 2R-1L'),
            [NumericTrait(value=3, left=1, right=2, start=0, end=13)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('embryo of 34402'),
            [])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('138-62-18-6  12.4g  scars  emb.1R,1L; '),
            [NumericTrait(value=2, left=1, right=1, start=27, end=36)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('; reproductive data=embryos: 4 right , 2 left  ;'),
            [NumericTrait(value=6, left=2, right=4, start=20, end=45)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('; reproductive data=embryos: 4 right , 2 left  ;'),
            [NumericTrait(value=6, left=2, right=4, start=20, end=45)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('7 embryos, 4 male, and 3 female'),
            [NumericTrait(value=7, male=4, female=3, start=0, end=31)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('reproductive data=5 embryos (3L, 2R);'),
            [NumericTrait(value=5, left=3, right=2, start=18, end=35)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('reproductive data=Vagina open.  4 small embryos.'),
            [NumericTrait(value=4, start=32, end=47)])

    def test_parse_12(self):
        self.assertEqual(
            PAR.parse('; 4 emb. x 07 mm, 3L2R", "weight":"23.0"'),
            [NumericTrait(value=4, left=3, right=2, start=2, end=22)])

    def test_parse_13(self):
        self.assertEqual(
            PAR.parse('; 3 emb. x 06 mm.",'),
            [NumericTrait(value=3, start=2, end=7)])

    def test_parse_14(self):
        self.assertEqual(
            PAR.parse('reproductive data: 3 embryos - 14 mm, 2R/1L;'),
            [NumericTrait(value=3, left=1, right=2, start=19, end=43)])

    def test_parse_15(self):
        self.assertEqual(
            PAR.parse('Med. nipples, no scars or embryos, mod. fat'),
            [NumericTrait(value=0, start=14, end=33)])

    def test_parse_16(self):
        self.assertEqual(
            PAR.parse('Fetus of AF 25577 (SHEID-99).'),
            [])

    def test_parse_17(self):
        self.maxDiff = None
        self.assertEqual(
            PAR.parse(', 4 fetuses on left, 1 on right'),
            [NumericTrait(value=5, left=4, right=1, start=2, end=31)])

    def test_parse_18(self):
        self.maxDiff = None
        self.assertEqual(
            PAR.parse('This specimen contained 4 fetuses'),
            [NumericTrait(value=4, start=24, end=33)])

    def test_parse_19(self):
        self.assertEqual(
            PAR.parse('; age class=fetus'),
            [])
