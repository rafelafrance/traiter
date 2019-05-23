import unittest
from traiter.parse import Parse
from traiter.traits.life_stage_trait import LifeStageTrait


PAR = None


class TestLifeStageTrait(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        global PAR
        PAR = LifeStageTrait()

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('sex=unknown ; age class=adult/juvenile after'),
            [Parse(value='adult/juvenile', start=14, end=38)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('age=u ad.'),
            [Parse(value='u ad', start=0, end=8)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse(
                'weight=5.2 g; age class=over-winter ; total length=99 mm;0'),
            [Parse(value='over-winter', start=14, end=37)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse(
                'sex=female ? ; age=1st year more than four words here'),
            [Parse(value='1st year', start=15, end=27)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('words after hatching year more words'),
            [Parse(value='after hatching year', start=6, end=25)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('age determined by 20-sided die'),
            [])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('LifeStage Remarks: 5-6 wks;'),
            [Parse(value='5-6 wks', start=0, end=27)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('mentions juvenile'),
            [Parse(value='juvenile', start=9, end=17)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('mentions juveniles in the field'),
            [Parse(value='juveniles', start=9, end=18)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('one or more adults'),
            [Parse(value='adults', start=12, end=18)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('adults'),
            [Parse(value='adults', start=0, end=6)])

    def test_parse_12(self):
        self.assertEqual(
            PAR.parse('Adulte'),
            [Parse(value='adulte', start=0, end=6)])

    def test_parse_13(self):
        self.assertEqual(
            PAR.parse('AGE IMM'),
            [Parse(value='imm', start=0, end=7)])

    def test_parse_14(self):
        self.assertEqual(
            PAR.parse('subadult'),
            [Parse(value='subadult', start=0, end=8)])

    def test_parse_15(self):
        self.assertEqual(
            PAR.parse('subadultery'),
            [])

    def test_parse_16(self):
        self.assertEqual(
            PAR.parse('in which larvae are found'),
            [Parse(value='larvae', start=9, end=15)])

    def test_parse_17(self):
        self.assertEqual(
            PAR.parse('one tadpole'),
            [Parse(value='tadpole', start=4, end=11)])

    def test_parse_18(self):
        # Lifestage removed
        self.assertEqual(
            PAR.parse('some embryos'),
            [])

    def test_parse_19(self):
        self.assertEqual(
            PAR.parse('young adult'),
            [Parse(value='young adult', start=0, end=11)])

    def test_parse_20(self):
        self.assertEqual(
            PAR.parse('adult young'),
            [Parse(value='adult', start=0, end=5),
             Parse(value='young', start=6, end=11)])

    def test_parse_21(self):
        self.assertEqual(
            PAR.parse('sub-adult'),
            [Parse(value='sub-adult', start=0, end=9)])

    def test_parse_22(self):
        self.assertEqual(
            PAR.parse('adult(s) and juvenile(s)'),
            [Parse(value='adult', start=0, end=5),
             Parse(value='juvenile', start=13, end=21)])

    def test_parse_23(self):
        self.assertEqual(
            PAR.parse('young-of-the-year'),
            [Parse(value='young-of-the-year', start=0, end=17)])

    def test_parse_24(self):
        self.assertEqual(
            PAR.parse('YOLK SAC'),
            [Parse(value='yolk sac', start=0, end=8)])

    def test_parse_25(self):
        self.assertEqual(
            PAR.parse('Specimen Age Estimate - minimum date: 15030'),
            [Parse(value='estimate - minimum date: 15030', start=9, end=43)])
