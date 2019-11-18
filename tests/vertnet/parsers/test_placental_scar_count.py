import unittest
from pylib.vertnet.numeric_trait import NumericTrait
from pylib.vertnet.parsers.placental_scar_count import PLACENTAL_SCAR_COUNT


class TestPlacentalScarCount(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('no emb; lactating; 7 plac scar'),
            [NumericTrait(value=7, start=19, end=30)])

    def test_parse_02(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse(
                'vagina imperforate; 5 plac scar 3L 2R'),
            [NumericTrait(value=5, left=3, right=2, start=20, end=37)])

    def test_parse_03(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('3 placental scars, 1L, 2R'),
            [NumericTrait(value=3, left=1, right=2, start=0, end=25)])

    def test_parse_04(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('4 plac scar'),
            [NumericTrait(value=4, start=0, end=11)])

    def test_parse_05(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('no placental scars'),
            [NumericTrait(value=0, start=0, end=18)])

    def test_parse_06(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('2+1=3 placental scars'),
            [NumericTrait(value=3, side1=2, side2=1, start=0, end=21)])

    def test_parse_07(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('U:P UTMD placental scar 1 + 2'),
            [NumericTrait(value=3, side1=1, side2=2, start=9, end=29)])

    def test_parse_08(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('uterus enlarged, scarring'),
            [NumericTrait(value='present', start=17, end=25)])

    def test_parse_09(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('VC, no embs, uterine scars'),
            [NumericTrait(value=0, start=4, end=26)])

    def test_parse_10(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('plac scar 1L'),
            [NumericTrait(value=1, left=1, start=0, end=12)])

    def test_parse_11(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('; 4 faint placental scars'),
            [NumericTrait(value=4, start=2, end=25)])

    def test_parse_12(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('5 plac scars: 3(R)&2(L)'),
            [NumericTrait(value=5, left=2, right=3, start=0, end=22)])

    def test_parse_13(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('2 placental scars, 0L, 2R'),
            [NumericTrait(value=2, left=0, right=2, start=0, end=25)])

    def test_parse_14(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('2+1=3 placental scars'),
            [NumericTrait(value=3, side1=2, side2=1, start=0, end=21)])

    def test_parse_15(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse(
                'not breeding, two scars, 1 left, 1 right'),
            [NumericTrait(value=2, left=1, right=1, start=18, end=40)])

    def test_parse_16(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('placental scars 1 + 1, mam tissue'),
            [NumericTrait(value=2, side1=1, side2=1, start=0, end=21)])

    def test_parse_17(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('2 P-SCAR R, 1 P-SCAR L'),
            [NumericTrait(value=3, left=1, right=2, start=0, end=22)])

    def test_parse_18(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('5 scars: 2lf,3rt'),
            [NumericTrait(value=5, left=2, right=3, start=0, end=16)])

    def test_parse_19(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('lactating, P-SCAR-R 3, P-SCAR-L 2'),
            [NumericTrait(value=5, left=2, right=3, start=11, end=33)])

    def test_parse_20(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('1R,0L plac scar'),
            [NumericTrait(value=1, left=0, right=1, start=0, end=15)])

    def test_parse_21(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('3 pac. scars:1(R)&2(L)'),
            [NumericTrait(value=3, left=2, right=1, start=0, end=21)])

    def test_parse_22(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('plac scar-9; lactating)'),
            [NumericTrait(value=9, start=0, end=11)])

    def test_parse_23(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse(
                '1 lt. plac. scar, 2 rt emb: CR: 16 mm'),
            [NumericTrait(value=3, left=1, right=2, start=0, end=22)])

    def test_parse_24(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('3+4= 7 placental scars'),
            [NumericTrait(value=7, side1=3, side2=4, start=0, end=22)])

    def test_parse_25(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('; no embroys or scar'),
            [NumericTrait(value=0, start=2, end=20)])

    def test_parse_26(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('; 3 prominent placental scars'),
            [NumericTrait(value=3, start=2, end=29)])

    def test_parse_27(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse(
                'VO, pg., 1 embryo (discarded), CRL+28 mm'),
            [])

    def test_parse_28(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('L 3 plac scars, R 2 pl. scars;'),
            [NumericTrait(value=5, left=3, right=2, start=0, end=29)])

    def test_parse_29(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse(
                'reproductive data=3R, 2L, placental scars;sex=female;'),
            [NumericTrait(value=5, left=2, right=3, start=18, end=41)])

    def test_parse_30(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse(
                'reproductive data=Scars - 5 on left, 5 of right'),
            [NumericTrait(value=10, left=5, right=5, start=18, end=47)])

    def test_parse_31(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse(
                ';reproductive data=Placental scars-2R; Embryos-1L,'),
            [NumericTrait(value=2, right=2, start=19, end=37)])

    def test_parse_32(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('no visible placental scarring'),
            [NumericTrait(value=0, start=0, end=29)])

    def test_parse_33(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('; 1 scar on tail ;'),
            [])

    def test_parse_34(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse(
                ', no scars horns R 2 plac scars, L 3 plac scars,'),
            [NumericTrait(start=2, end=10, value=0),
             NumericTrait(start=17, end=47, value=5, right=2, left=3)])

    def test_parse_35(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse(
                'reproductive data=perf, pelvis not sep, nipples large, '
                'horns R+L1.5wide 2+plac. scars,'),
            [NumericTrait(value='present', start=74, end=85)])

    def test_parse_36(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse(
                '; sex=female ; reproductive data=scars  0R-4L ;'),
            [NumericTrait(value=4, left=4, right=0, start=33, end=45)])

    def test_parse_37(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse(
                'SKULL CLEANED AT ILLINOIS STATE MUSEUM OCT 95; '
                'SCAR ABOVE TAIL, EVIDENCE OF PAST INSECT DAMAGE;'),
            [])

    def test_parse_38(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse(
                'ut horns: R 1 definite scar, L 2+ scars;'),
            [NumericTrait(value=3, left=2, right=1, start=10, end=39)])

    def test_parse_39(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('DINO 14431; placental scars'),
            [NumericTrait(value='present', start=12, end=27)])

    def test_parse_40(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse(
                '"Note in catalog: same as 135478";Scarritt '
                'Venezuelan Exped."'),
            [])

    def test_parse_41(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('5 ut scars, 132-62-20-15=19'),
            [NumericTrait(value=5, start=0, end=10)])

    def test_parse_42(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse(
                'specimen number AJU 372; P-SCAR-R 5, P-SCAR-L 5'),
            [NumericTrait(value=10, left=5, right=5, start=25, end=47)])

    def test_parse_43(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse(
                'Zion 11396; NK 36683; scars/no embs/lact'),
            [NumericTrait(value='present', start=22, end=27)])

    def test_parse_44(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse(
                'negative for nematodes; skull labeled 14 Nov 57. PSM: '
                'Mamm Puget Sound Museum ID 27461'),
            [])

    def test_parse_45(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse(
                "born in lab on Sept 3 to 7 '56; placed in sep. cage 28 "
                "Sept 56; skull labeled 23 Jan 57"),
            [])

    def test_parse_46(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse('H,K,L,L,S; UTERINE SCARS=2R'),
            [NumericTrait(value=2, right=2, start=11, end=27)])

    def test_parse_47(self):
        self.assertEqual(
            PLACENTAL_SCAR_COUNT.parse(
                'no embryonic scars 360-40-125-68 1800g'),
            [NumericTrait(value=0, start=0, end=18)])
