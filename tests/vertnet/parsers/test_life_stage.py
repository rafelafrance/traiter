import unittest
from pylib.vertnet.trait import Trait
from pylib.vertnet.parsers.life_stage import LIFE_STAGE


class TestLifeStage(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            LIFE_STAGE.parse('sex=unknown ; age class=adult/juvenile after'),
            [Trait(value='adult/juvenile', start=14, end=38)])

    def test_parse_02(self):
        self.assertEqual(
            LIFE_STAGE.parse('age=u ad.'),
            [Trait(value='u ad.', start=0, end=9)])

    def test_parse_03(self):
        self.assertEqual(
            LIFE_STAGE.parse(
                'weight=5.2 g; age class=over-winter ; total length=99 mm;0'),
            [Trait(value='over-winter', start=14, end=37)])

    def test_parse_04(self):
        self.assertEqual(
            LIFE_STAGE.parse(
                'sex=female ? ; age=1st year more than four words here'),
            [Trait(value='1st year', start=15, end=27)])

    def test_parse_05(self):
        self.assertEqual(
            LIFE_STAGE.parse('words after hatching year more words'),
            [Trait(value='after hatching year', start=6, end=25)])

    def test_parse_06(self):
        self.assertEqual(
            LIFE_STAGE.parse('age determined by 20-sided die'),
            [])

    def test_parse_07(self):
        self.assertEqual(
            LIFE_STAGE.parse('LifeStage Remarks: 5-6 wks;'),
            [Trait(value='5-6 wks', start=0, end=27)])

    def test_parse_08(self):
        self.assertEqual(
            LIFE_STAGE.parse('mentions juvenile'),
            [Trait(value='juvenile', start=9, end=17)])

    def test_parse_09(self):
        self.assertEqual(
            LIFE_STAGE.parse('mentions juveniles in the field'),
            [Trait(value='juveniles', start=9, end=18)])

    def test_parse_10(self):
        self.assertEqual(
            LIFE_STAGE.parse('one or more adults'),
            [Trait(value='adults', start=12, end=18)])

    def test_parse_11(self):
        self.assertEqual(
            LIFE_STAGE.parse('adults'),
            [Trait(value='adults', start=0, end=6)])

    def test_parse_12(self):
        self.assertEqual(
            LIFE_STAGE.parse('Adulte'),
            [Trait(value='adulte', start=0, end=6)])

    def test_parse_13(self):
        self.assertEqual(
            LIFE_STAGE.parse('AGE IMM'),
            [Trait(value='imm', start=0, end=7)])

    def test_parse_14(self):
        self.assertEqual(
            LIFE_STAGE.parse('subadult'),
            [Trait(value='subadult', start=0, end=8)])

    def test_parse_15(self):
        self.assertEqual(
            LIFE_STAGE.parse('subadultery'),
            [])

    def test_parse_16(self):
        self.assertEqual(
            LIFE_STAGE.parse('in which larvae are found'),
            [Trait(value='larvae', start=9, end=15)])

    def test_parse_17(self):
        self.assertEqual(
            LIFE_STAGE.parse('one tadpole'),
            [Trait(value='tadpole', start=4, end=11)])

    def test_parse_18(self):
        # Life stage removed
        self.assertEqual(
            LIFE_STAGE.parse('some embryos'),
            [])

    def test_parse_19(self):
        self.assertEqual(
            LIFE_STAGE.parse('young adult'),
            [Trait(value='young adult', start=0, end=11)])

    def test_parse_20(self):
        self.assertEqual(
            LIFE_STAGE.parse('adult young'),
            [Trait(value='adult young', start=0, end=11)])

    def test_parse_21(self):
        self.assertEqual(
            LIFE_STAGE.parse('sub-adult'),
            [Trait(value='sub-adult', start=0, end=9)])

    def test_parse_22(self):
        self.assertEqual(
            LIFE_STAGE.parse('adult(s) and juvenile(s)'),
            [Trait(value='adult', start=0, end=5),
             Trait(value='juvenile', start=13, end=21)])

    def test_parse_23(self):
        self.assertEqual(
            LIFE_STAGE.parse('young-of-the-year'),
            [Trait(value='young-of-the-year', start=0, end=17)])

    def test_parse_24(self):
        self.assertEqual(
            LIFE_STAGE.parse('YOLK SAC'),
            [Trait(value='yolk sac', start=0, end=8)])

    def test_parse_25(self):
        self.assertEqual(
            LIFE_STAGE.parse('Specimen Age Estimate - minimum date: 15030'),
            [Trait(value='estimate - minimum date: 15030', start=9, end=43)])
