import unittest
from lib.trait import Trait
from lib.trait_builders.nipple_state_trait_builder \
    import NippleStateTraitBuilder


PAR = None


class TestSexTraitBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global PAR
        PAR = NippleStateTraitBuilder()

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('vagina closed, nipples large'),
            [Trait(value='nipples large', start=15, end=28)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('pregnant; 5 emb; protuberant nipples'),
            [Trait(value='protuberant nipples', start=17, end=36)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('NO nipple showing'),
            [Trait(value='no nipple showing', start=0, end=17)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('no emb; VERY SMALL FALSE NIPPLES'),
            [Trait(value='very small false nipples', start=8, end=32)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('; NIPPLES INDICATE PREVIOUS LACTATION'),
            [Trait(
                value='nipples indicate previous lactation', start=2, end=37)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('Nipples slightly enlarged.'),
            [Trait(value='nipples slightly enlarged', start=0, end=25)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('Nipples pigmented.'),
            [Trait(value='nipples pigmented', start=0, end=17)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('no scars or emb., nip. sm., low fat'),
            [Trait(value='nip. sm', start=18, end=25)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('; teats visible,'),
            [Trait(value='teats visible', start=2, end=15)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('10 post-lactating teats'),
            [Trait(value='post-lactating teats', start=3, end=23)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse(', LG UTERUS & TEATS,'),
            [Trait(value='lg uterus & teats', start=2, end=19)])

    def test_parse_12(self):
        self.assertEqual(
            PAR.parse('4 teats post lac.'),
            [Trait(value='teats post lac', start=2, end=16)])

    def test_parse_13(self):
        self.assertEqual(
            PAR.parse('lactating, mammary glands much swollen'),
            [Trait(value='mammary glands much swollen', start=11, end=38)])

    def test_parse_14(self):
        self.assertEqual(
            PAR.parse('; mammary tissue present;'),
            [Trait(value='mammary tissue present', start=2, end=24)])

    def test_parse_15(self):
        self.assertEqual(
            PAR.parse('VO, NE, mamm. lg.'),
            [Trait(value='mamm. lg', start=8, end=16)])

    def test_parse_16(self):
        self.assertEqual(
            PAR.parse('mammary glands active'),
            [Trait(value='mammary glands active', start=0, end=21)])

    def test_parse_17(self):
        self.assertEqual(
            PAR.parse('vagina opened, well developed mammary tissue'),
            [Trait(value='well developed mammary tissue', start=15, end=44)])

    def test_parse_18(self):
        self.assertEqual(
            PAR.parse('mammae conspicuous; lactating;'),
            [Trait(value='mammae conspicuous', start=0, end=18)])

    def test_parse_19(self):
        self.assertEqual(
            PAR.parse('; MAMMARY TISSSUE ABSENT;'),
            [Trait(value='mammary tisssue absent', start=2, end=24)])

    def test_parse_20(self):
        self.assertEqual(
            PAR.parse('; reproductive data=no nipples showing, uterus found;'),
            [Trait(value='no nipples showing', start=20, end=38)])
