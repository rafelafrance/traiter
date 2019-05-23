import unittest
from traiter.parse import Parse
from traiter.traits.ovaries_state_trait import OvariesStateTrait


PAR = None


class TestOvariesStateTrait(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        global PAR
        PAR = OvariesStateTrait()

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse(
                'sex=female ; '
                'reproductive data=Ovaries and uterus small, immature'),
            [Parse(value='small, immature', start=31, end=65)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse(
                'sex=female ; '
                'reproductive data=OVARIES ENLARGED - 7X12 MM, LACTATING'),
            [Parse(value='enlarged', start=31, end=47)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('reproductive data=ovaries and uterine horns '
                      'covered with copious fat ;'),
            [Parse(value='covered with copious fat', start=18, end=68)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('; ovaries mod size;'),
            [Parse(value='mod size', start=2, end=18)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('; +corp. alb both ovaries;'),
            [Parse(value='+corp. alb', side='both', start=2, end=25)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('ovaries: R 2 c. alb, L sev c. alb;'),
            [Parse(value='c. alb', side='r', start=0, end=33),
             Parse(value='sev c. alb', side='l', start=0, end=33)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('ovaries immature;'),
            [Parse(value='immature', start=0, end=16)])

    def test_parse_08(self):
        self.maxDiff = None
        self.assertEqual(
            PAR.parse('reproductive data=Ovary, fallopian tubes dark red.'),
            [Parse(value='dark red', start=18, end=49)])

    def test_parse_09(self):
        self.assertEqual(
                PAR.parse('reproductive data=Left ovary=3x1.5mm, '
                          'pale pink in color; uterus thin'),
                [Parse(value='pale pink', side='left', start=18, end=47)])

    def test_parse_10(self):
        self.maxDiff = None
        self.assertEqual(
                PAR.parse(', ovaries immature (no lg folls) ;'),
                [Parse(value='immature', start=2, end=18)])


