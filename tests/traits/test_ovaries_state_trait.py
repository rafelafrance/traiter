import unittest
from lib.parse import Parse
from lib.traits.ovaries_state_trait import OvariesStateTrait


PAR = OvariesStateTrait()


class TestOvariesStateTrait(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse(
                'sex=female ; '
                'reproductive data=Ovaries and uterus small, immature'),
            [Parse(value='small', start=31, end=55)])

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
            [Parse(value='+corp. alb both', start=2, end=25)])

    def test_parse_06(self):
        self.maxDiff = None
        self.assertEqual(
            PAR.parse('ovaries: R 2 c. alb, L sev c. alb;'),
            [Parse(value='c. alb', side='r', start=0, end=33),
             Parse(value='sev c. alb', side='l', start=0, end=33)])

