import unittest
from pylib.vertnet.trait import Trait
from pylib.vertnet.parsers.ovaries_state import OVARIES_STATE


class TestOvariesState(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            OVARIES_STATE.parse(
                'sex=female ; '
                'reproductive data=Ovaries and uterus small, immature'),
            [Trait(value='small, immature', start=31, end=65)])

    def test_parse_02(self):
        self.assertEqual(
            OVARIES_STATE.parse(
                'sex=female ; '
                'reproductive data=OVARIES ENLARGED - 7X12 MM, LACTATING'),
            [Trait(value='enlarged', start=31, end=47)])

    def test_parse_03(self):
        self.assertEqual(
            OVARIES_STATE.parse(
                'reproductive data=ovaries and uterine horns '
                'covered with copious fat ;'),
            [Trait(value='covered with copious fat', start=18, end=68)])

    def test_parse_04(self):
        self.assertEqual(
            OVARIES_STATE.parse('; ovaries mod size;'),
            [Trait(value='mod size', start=2, end=18)])

    def test_parse_05(self):
        self.assertEqual(
            OVARIES_STATE.parse(
                'reproductive data=L ov 2 lg foll + 2 c.l.; '
                'R ov 3 c.l.; L horn 4 dark scars, 3 lt; '
                'R horn 6 dark, 6 lt; +corp. alb both ovaries;'),
            [
                Trait(value='lg foll', side='l', start=18, end=32),
                Trait(value='c.l.', side='r', start=43, end=54),
                Trait(value='+corp. alb', side='both', start=104, end=127),
            ])

    def test_parse_06(self):
        self.assertEqual(
            OVARIES_STATE.parse('ovaries: R 2 c. alb, L sev c. alb;'),
            [Trait(value='c. alb', side='r', start=0, end=33),
             Trait(value='sev c. alb', side='l', start=0, end=33)])

    def test_parse_07(self):
        self.assertEqual(
            OVARIES_STATE.parse('ovaries immature;'),
            [Trait(value='immature', start=0, end=16)])

    def test_parse_08(self):
        self.assertEqual(
            OVARIES_STATE.parse(
                'reproductive data=Ovary, fallopian tubes dark red.'),
            [Trait(value='fallopian tubes dark red', start=18, end=49)])

    def test_parse_09(self):
        self.assertEqual(
            OVARIES_STATE.parse(
                'reproductive data=Left ovary=3x1.5mm, '
                'pale pink in color; uterus thin'),
            [Trait(value='pale pink', side='left', start=18, end=47)])

    def test_parse_10(self):
        self.assertEqual(
            OVARIES_STATE.parse(', ovaries immature (no lg folls) ;'),
            [Trait(value='immature', start=2, end=18)])

    def test_parse_11(self):
        self.assertEqual(
            OVARIES_STATE.parse(
                'reproductive data=Ovaries and uterus small, immature'),
            [Trait(value='small, immature', start=18, end=52)])

    def test_parse_12(self):
        self.assertEqual(
            OVARIES_STATE.parse('ovaries mod size;'),
            [Trait(value='mod size', start=0, end=16)])

    def test_parse_13(self):
        self.assertEqual(
            OVARIES_STATE.parse(
                'reproductive data=Ovaries minute, not embryos.'),
            [Trait(value='minute', start=18, end=32)])

    def test_parse_14(self):
        self.assertEqual(
            OVARIES_STATE.parse('; both ovaries sev c.alb.;'),
            [Trait(value='sev c.alb', side='both', start=2, end=24)])

    def test_parse_15(self):
        self.assertEqual(
            OVARIES_STATE.parse(
                'reproductive data=pelvis fused, ovaries inactive;'),
            [Trait(value='inactive', start=32, end=48)])

    def test_parse_16(self):
        self.assertEqual(
            OVARIES_STATE.parse('reproductive data=right ovary destroyed ;'),
            [Trait(value='destroyed', side='right', start=18, end=39)])

    def test_parse_17(self):
        self.assertEqual(
            OVARIES_STATE.parse('reproductive data=large ovaries ;'),
            [Trait(value='large', start=18, end=31)])

    def test_parse_18(self):
        self.assertEqual(
            OVARIES_STATE.parse('ovaries somewhat enlarged'),
            [Trait(value='somewhat enlarged', start=0, end=25)])

    def test_parse_19(self):
        self.assertEqual(
            OVARIES_STATE.parse('ovaries imm.'),
            [Trait(value='imm', start=0, end=11)])

    def test_parse_20(self):
        self.assertEqual(
            OVARIES_STATE.parse('ovaries: both w/sev c. alb;'),
            [Trait(value='sev c. alb', side='both', start=0, end=26)])

    def test_parse_21(self):
        self.assertEqual(
            OVARIES_STATE.parse('corpus luteum visible in both ovaries'),
            [Trait(
                value='corpus luteum visible', side='both',
                start=0, end=37)])

    def test_parse_22(self):
        self.assertEqual(
            OVARIES_STATE.parse(
                'reproductive data=only 1 fully developed ovary ;'),
            [Trait(value='fully developed', start=25, end=46)])

    def test_parse_23(self):
        self.assertEqual(
            OVARIES_STATE.parse('ovaries shrunken'),
            [Trait(value='shrunken', start=0, end=16)])

    def test_parse_24(self):
        self.assertEqual(
            OVARIES_STATE.parse('inactive ovary'),
            [Trait(value='inactive', start=0, end=14)])

    def test_parse_25(self):
        self.assertEqual(
            OVARIES_STATE.parse('no embryos, nips small, ovary < 1 x 1 mm'),
            [])

    def test_parse_26(self):
        self.assertEqual(
            OVARIES_STATE.parse('Cyst on ovary'),
            [Trait(value='cyst on', start=0, end=13)])

    def test_parse_27(self):
        self.assertEqual(
            OVARIES_STATE.parse('; 4 bodies in L ovary;'),
            [Trait(value='4 bodies in', side='l', start=2, end=21)])

    def test_parse_28(self):
        self.assertEqual(
            OVARIES_STATE.parse('Mod. fat, ovaries black'),
            [Trait(value='black', start=10, end=23)])

    def test_parse_29(self):
        self.assertEqual(
            OVARIES_STATE.parse('ovary not seen'),
            [Trait(value='not seen', start=0, end=14)])

    def test_parse_30(self):
        self.assertEqual(
            OVARIES_STATE.parse('ovaries pink, fat'),
            [Trait(value='pink', start=0, end=12)])

    def test_parse_31(self):
        self.assertEqual(
            OVARIES_STATE.parse('Left side of ovaries large and cancerous'),
            [Trait(
                value='large and cancerous', start=13, end=40)])

    def test_parse_32(self):
        self.assertEqual(
            OVARIES_STATE.parse(
                'ovaries well developed, but not pregnant apparently;'),
            [Trait(value='well developed', start=0, end=22)])

    def test_parse_33(self):
        self.assertEqual(
            OVARIES_STATE.parse(
                'ovaries pink and smooth, fat around base of '
                'tail and oviduct'),
            [Trait(value='pink and smooth', start=0, end=23)])

    def test_parse_34(self):
        self.assertEqual(
            OVARIES_STATE.parse(
                'Yng. 7 blastocysts and 2 ovaries preserved (where?)'),
            [])

    def test_parse_35(self):
        self.assertEqual(
            OVARIES_STATE.parse(
                'reproductive data=imp, pelv fused, nipp tiny, nullip, '
                'both ov w/ few sm foll;'),
            [Trait(value='few sm foll', side='both', start=54, end=76)])

    def test_parse_36(self):
        self.assertEqual(
            OVARIES_STATE.parse(
                'stomach, jaw, claw, ovaries, womb too large to preserve'),
            [])

    def test_parse_37(self):
        self.assertEqual(
            OVARIES_STATE.parse(
                'Rov 3 cl, Lov 4 cl, both ov sm-med foll; no molt no scars;'),
            [Trait(value='sm-med foll', side='both', start=20, end=39)])
