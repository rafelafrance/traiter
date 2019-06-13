import unittest
from traiter.trait import Trait
from traiter.trait_builders.ovaries_state_trait_builder \
    import OvariesStateTraitBuilder


PAR = None


class TestOvariesStateTraitBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global PAR
        PAR = OvariesStateTraitBuilder()

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse(
                'sex=female ; '
                'reproductive data=Ovaries and uterus small, immature'),
            [Trait(value='small, immature', start=31, end=65)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse(
                'sex=female ; '
                'reproductive data=OVARIES ENLARGED - 7X12 MM, LACTATING'),
            [Trait(value='enlarged', start=31, end=47)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('reproductive data=ovaries and uterine horns '
                      'covered with copious fat ;'),
            [Trait(value='covered with copious fat', start=18, end=68)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('; ovaries mod size;'),
            [Trait(value='mod size', start=2, end=18)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('; +corp. alb both ovaries;'),
            [Trait(value='+corp. alb', side='both', start=2, end=25)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('ovaries: R 2 c. alb, L sev c. alb;'),
            [Trait(value='c. alb', side='r', start=0, end=33),
             Trait(value='sev c. alb', side='l', start=0, end=33)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('ovaries immature;'),
            [Trait(value='immature', start=0, end=16)])

    def test_parse_08(self):
        self.maxDiff = None
        self.assertEqual(
            PAR.parse('reproductive data=Ovary, fallopian tubes dark red.'),
            [Trait(value='dark red', start=18, end=49)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('reproductive data=Left ovary=3x1.5mm, '
                      'pale pink in color; uterus thin'),
            [Trait(value='pale pink', side='left', start=18, end=47)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse(', ovaries immature (no lg folls) ;'),
            [Trait(value='immature', start=2, end=18)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse(
                'reproductive data=Ovaries and uterus small, immature'),
            [Trait(value='small, immature', start=18, end=52)])

    def test_parse_12(self):
        self.assertEqual(
            PAR.parse('ovaries mod size;'),
            [Trait(value='mod size', start=0, end=16)])


if __name__ == '__main__':
    unittest.main()
