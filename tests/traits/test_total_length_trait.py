# pylint: disable=missing-docstring,too-many-public-methods

import unittest
from lib.parse import Parse
from lib.traits.total_length_trait import TotalLengthTrait


PAR = TotalLengthTrait()


class TestTotalLengthTrait(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('{"totalLengthInMM":"123" };'),
            [Parse(value=123, units='mm', start=2, end=23)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('measurements: ToL=230;TaL=115;HF=22;E=18;'
                      ' total length=231 mm; tail length=115 mm;'),
            [Parse(value=230, units_inferred=True, start=14, end=21),
             Parse(value=231, units='mm', start=42, end=61)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('measurements: ToL=230;TaL=115;HF=22;E=18;'
                      ' total length=24 cm; tail length=115 mm;'),
            [Parse(value=230, units_inferred=True, start=14, end=21),
             Parse(value=240, units='cm', start=42, end=60)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('sex=unknown ; crown-rump length=8 mm'),
            [])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('left gonad length=10 mm; right gonad length=10 mm;'),
            [])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('"{"measurements":"308-190-45-20" }"'),
            [Parse(value=308, units='mm_shorthand', start=3, end=31)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('308-190-45-20'),
            [Parse(value=308, units='mm_shorthand', start=0, end=13)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse((
                'snout-vent length=54 mm; total length=111 mm;'
                ' tail length=57 mm; weight=5 g')),
            [Parse(value=54, units='mm', start=0, end=23),
             Parse(value=111, units='mm', start=25, end=44)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse((
                'unformatted measurements=Verbatim weight=X;'
                'ToL=230;TaL=115;HF=22;E=18;'
                ' total length=231 mm; tail length=115 mm;')),
            [Parse(value=230, units_inferred=True, start=43, end=50),
             Parse(value=231, units='mm', start=71, end=90)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('143-63-20-17=13'),
            [Parse(value=143, units='mm_shorthand', start=0, end=15)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('** Body length =345 cm; Blubber=1 cm '),
            [Parse(value=3450, units='cm', start=3, end=22)])

    def test_parse_12(self):
        self.assertEqual(
            PAR.parse('t.l.= 2 feet 3.1 - 4.5 inches '),
            [Parse(value=[688.34, 723.9], units=['ft', 'in'],
                   start=0, end=29)])

    def test_parse_13(self):
        self.assertEqual(
            PAR.parse('2 ft. 3.1 - 4.5 in. '),
            [Parse(value=[688.34, 723.9], ambiguous_key=True,
                   units=['ft', 'in'], start=0, end=18)])

    def test_parse_14(self):
        self.assertEqual(
            PAR.parse('total length= 2 ft.'),
            [Parse(value=609.6, units='ft', start=0, end=18)])

    def test_parse_15(self):
        self.assertEqual(
            PAR.parse('AJR-32   186-102-23-15  15.0g'),
            [Parse(value=186, units='mm_shorthand', start=9, end=29)])

    def test_parse_16(self):
        self.assertEqual(
            PAR.parse('length=8 mm'),
            [Parse(value=8, units='mm', ambiguous_key=True,
                   start=0, end=11)])

    def test_parse_17(self):
        self.assertEqual(
            PAR.parse('another; length=8 mm'),
            [Parse(value=8, units='mm', ambiguous_key=True,
                   start=9, end=20)])

    def test_parse_18(self):
        self.assertEqual(
            PAR.parse('another; TL_120, noise'),
            [Parse(value=120, units_inferred=True,
                   start=9, end=15)])

    def test_parse_19(self):
        self.assertEqual(
            PAR.parse('another; TL - 101.3mm, noise'),
            [Parse(value=101.3, units='mm', start=9, end=21)])

    def test_parse_20(self):
        self.assertEqual(
            PAR.parse('before; TL153, after'),
            [Parse(value=153, units_inferred=True,
                   start=8, end=13)])

    def test_parse_21(self):
        self.assertEqual(
            PAR.parse((
                'before; Total length in catalog and '
                'specimen tag as 117, after')),
            [])

    def test_parse_22(self):
        self.assertEqual(
            PAR.parse('before Snout vent lengths range from 16 to 23 mm. qq'),
            [Parse(value=[16, 23], units='mm', start=7, end=48)])

    def test_parse_23(self):
        self.assertEqual(
            PAR.parse('Size=13 cm TL'),
            [Parse(value=130, units='cm', start=5, end=13)])

    def test_parse_24(self):
        self.assertEqual(
            PAR.parse('det_comments:31.5-58.3inTL'),
            [Parse(
                value=[800.1, 1480.82], units='in', start=13, end=26)])

    def test_parse_25(self):
        self.assertEqual(
            PAR.parse('SVL52mm'),
            [Parse(value=52, units='mm', start=0, end=7)])

    def test_parse_26(self):
        self.assertEqual(
            PAR.parse('snout-vent length=221 mm; total length=257 mm; '
                      'tail length=36 mm'),
            [Parse(value=221, units='mm', start=0, end=24),
             Parse(value=257, units='mm', start=26, end=45)])

    def test_parse_27(self):
        self.assertEqual(
            PAR.parse('SVL 209 mm, total 272 mm, 4.4 g.'),
            [Parse(value=209, units='mm', start=0, end=10),
             Parse(value=272, units='mm', start=12, end=24)])

    def test_parse_28(self):
        self.assertEqual(
            PAR.parse('{"time collected":"0712-0900", "length":"12.0" }'),
            [Parse(value=12, ambiguous_key=True, units_inferred=True,
                   start=32, end=45)])

    def test_parse_29(self):
        self.assertEqual(
            PAR.parse('{"time collected":"1030", "water depth":"1-8", '
                      '"bottom":"abrupt lava cliff dropping off to sand at '
                      '45 ft.", "length":"119-137" }'),
            [Parse(value=[119, 137], ambiguous_key=True, units_inferred=True,
                   start=109, end=125)])

    def test_parse_30(self):
        self.assertEqual(
            PAR.parse('TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx'),
            [Parse(value=44, units='mm', start=0, end=10),
             Parse(value=38, units='mm', start=11, end=21)])

    def test_parse_31(self):
        self.assertEqual(
            PAR.parse('{"totalLengthInMM":"270-165-18-22-31", '),
            [Parse(value=270, units='mm_shorthand', start=20, end=36)])

    def test_parse_32(self):
        self.assertEqual(
            PAR.parse('{"length":"20-29" }'),
            [Parse(value=[20, 29], ambiguous_key=True, units_inferred=True,
                   start=2, end=16)])

    def test_parse_33(self):
        self.assertEqual(
            PAR.parse('field measurements on fresh dead specimen were '
                      '157-60-20-19-21g'),
            [Parse(value=157, units='mm_shorthand', start=47, end=63)])

    def test_parse_34(self):
        self.assertEqual(
            PAR.parse('f age class: adult; standard length: 63-107mm'),
            [Parse(value=[63, 107], units='mm', start=20, end=45)])

    def test_parse_35(self):
        self.assertEqual(
            PAR.parse('Rehydrated in acetic acid 7/1978-8/1987.'),
            [])

    def test_parse_36(self):
        self.assertEqual(
            PAR.parse('age class: adult; standard length: 18.0-21.5mm'),
            [Parse(value=[18, 21.5], units='mm', start=18, end=46)])

    def test_parse_37(self):
        self.assertEqual(
            PAR.parse('age class: adult; standard length: 18-21.5mm'),
            [Parse(value=[18, 21.5], units='mm', start=18, end=44)])

    def test_parse_38(self):
        self.assertEqual(
            PAR.parse('age class: adult; standard length: 18.0-21mm'),
            [Parse(value=[18, 21], units='mm', start=18, end=44)])

    def test_parse_39(self):
        self.assertEqual(
            PAR.parse('age class: adult; standard length: 18-21mm'),
            [Parse(value=[18, 21], units='mm', start=18, end=42)])

    def test_parse_40(self):
        self.assertEqual(
            PAR.parse(
                "Specimen #'s - 5491,5492,5498,5499,5505,5526,5527,5528,5500,"
                "5507,5508,5590,5592,5595,5594,5593,5596,5589,5587,5586,5585"),
            [])

    def test_parse_41(self):
        self.assertEqual(
            PAR.parse('20-28mm SL'),
            [Parse(value=[20, 28], units='mm', start=0, end=10)])

    def test_parse_42(self):
        self.assertEqual(
            PAR.parse('29mm SL'),
            [Parse(value=29, units='mm', start=0, end=7)])

    def test_parse_43(self):
        self.assertEqual(
            PAR.parse('{"measurements":"159-?-22-16=21.0" }'),
            [Parse(value=159, units='mm_shorthand', start=2, end=33)])

    def test_parse_44(self):
        self.assertEqual(
            PAR.parse('c701563b-dbd9-4500-184f-1ad61eb8da11'),
            [])

    def test_parse_45(self):
        self.assertEqual(
            PAR.parse('Meas: L: 21.0'),
            [Parse(value=21, units_inferred=True,
                   start=0, end=13)])

    def test_parse_46(self):
        self.assertEqual(
            PAR.parse('Meas: L: 21.0 cm'),
            [Parse(value=210, units='cm', start=0, end=16)])

    def test_parse_47(self):
        self.assertEqual(
            PAR.parse('LABEL. LENGTH 375 MM.'),
            [Parse(value=375, units='mm', start=0, end=20)])

    def test_parse_48(self):
        self.assertEqual(
            PAR.parse('SL=12mm'),
            [Parse(value=12, units='mm', start=0, end=7)])

    def test_parse_49(self):
        self.assertEqual(
            PAR.parse('Size=SL 12-14 mm'),
            [Parse(value=[12, 14], units='mm', start=5, end=16)])

    def test_parse_50(self):
        self.assertEqual(
            PAR.parse('SV 1.2'),
            [Parse(value=1.2, units_inferred=True,
                   start=0, end=6)])

    def test_parse_51(self):
        self.assertEqual(
            PAR.parse(' Length: 123 mm SL'),
            [Parse(value=123, units='mm', start=1, end=18)])

    def test_parse_52(self):
        self.assertEqual(
            PAR.parse(' Length: 12-34 mmSL'),
            [Parse(value=[12, 34], units='mm', start=1, end=19)])

    def test_parse_53(self):
        self.assertEqual(
            PAR.parse('Measurements: L: 21.0 cm'),
            [Parse(value=210, units='cm', start=0, end=24)])

    def test_parse_54(self):
        self.assertEqual(
            PAR.parse('SVL=44'),
            [Parse(value=44, units_inferred=True,
                   start=0, end=6)])

    def test_parse_55(self):
        self.assertEqual(
            PAR.parse('SVL=0 g'),
            [Parse(value=0, units_inferred=True,
                   start=0, end=5)])

    def test_parse_56(self):
        self.assertEqual(
            PAR.parse('SVL=44'),
            [Parse(value=44, units_inferred=True,
                   start=0, end=6)])

    def test_parse_57(self):
        self.assertEqual(
            PAR.parse('TL=50'),
            [Parse(value=50, units_inferred=True,
                   start=0, end=5)])

    def test_parse_58(self):
        self.assertEqual(
            PAR.parse('SVL=44mm'),
            [Parse(value=44, units='mm', start=0, end=8)])

    def test_parse_59(self):
        # Infer the units from other measurements in post processing
        self.assertEqual(
            PAR.parse('SV 1.4, TAIL 1.0 CM. HATCHLING'),
            [Parse(value=1.4, units_inferred=True,
                   start=0, end=6)])

    def test_parse_60(self):
        self.assertEqual(
            PAR.parse('LENGTH 10 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN.'),
            [Parse(
                value=263.52,
                ambiguous_key=True, units='in',
                start=0, end=16)])

    def test_parse_61(self):
        self.assertEqual(
            PAR.parse(
                ('tail length in mm: -; total length in mm: -; '
                 'wing chord in mm: 81.0R; wing spread in mm: -')),
            [])

    def test_parse_62(self):
        self.assertEqual(
            PAR.parse('76 cm S.L., 4.7 kg'),
            [Parse(value=760, units='cm', start=0, end=10)])

    def test_parse_63(self):
        self.assertEqual(
            PAR.parse('set mark: 661 1-5 64-61'),
            [])

    def test_parse_64(self):
        self.assertEqual(
            PAR.parse('{"totalLength":"970", "wing":"390" }'),
            [Parse(value=970, units_inferred=True,
                   start=2, end=19)])

    def test_parse_65(self):
        self.assertEqual(
            PAR.parse('LENGTH: 117MM. SOFT PARTS COLOR ON LABEL.'),
            [Parse(value=117, units='mm', ambiguous_key=True,
                   start=0, end=13)])

    def test_parse_66(self):
        self.assertEqual(
            PAR.parse('Meas:Length (L): 5'),
            [Parse(value=5, units_inferred=True,
                   start=0, end=18)])

    def test_parse_67(self):
        self.assertEqual(
            PAR.parse('Size=41-148mm SL'),
            [Parse(value=[41, 148], units='mm', start=5, end=16)])

    def test_parse_68(self):
        self.assertEqual(
            PAR.parse('Size=105 mm TL, 87.1 mm PCL'),
            [Parse(value=105, units='mm', start=5, end=14)])

    def test_parse_69(self):
        self.assertEqual(
            PAR.parse('Total Length: 185-252 mm'),
            [Parse(value=[185, 252], units='mm', start=0, end=24)])

    def test_parse_70(self):
        self.assertEqual(
            PAR.parse('Total Length: 185 - 252 mm'),
            [Parse(value=[185, 252], units='mm', start=0, end=26)])

    def test_parse_71(self):
        self.assertEqual(
            PAR.parse('"bottom":"rock?", "length":"278" }'),
            [Parse(value=278, ambiguous_key=True, units_inferred=True,
                   start=19, end=31)])

    def test_parse_72(self):
        self.assertEqual(
            PAR.parse('[308]-190-45-20'),
            [Parse(value=308, units='mm_shorthand',
                   estimated_value=True, start=0, end=15)])

    def test_parse_73(self):
        self.assertEqual(
            PAR.parse('"{"measurements":"[308]-190-45-20" }"'),
            [Parse(value=308, units='mm_shorthand',
                   estimated_value=True,
                   start=3, end=33)])

    def test_parse_74(self):
        self.assertEqual(
            PAR.parse('308-190-45-20-11-22'),
            [])

    def test_parse_75(self):
        self.assertEqual(
            PAR.parse('10 12/07/1944'),
            [])

    def test_parse_76(self):
        self.assertEqual(
            PAR.parse('12-07-1944'),
            [])

    def test_parse_77(self):
        self.assertEqual(
            PAR.parse('{"measurements":"210-92-30" }'),
            [Parse(value=210, units='mm_shorthand', start=2, end=26)])

    def test_parse_78(self):
        self.assertEqual(
            PAR.parse('measurements:210-92-30 308-190-45-20'),
            [Parse(value=308, units='mm_shorthand', start=23, end=36)])

    def test_parse_79(self):
        self.assertEqual(
            PAR.parse('measurements:210-92-30 185-252 mm'),
            [Parse(value=[185, 252], units='mm', start=0, end=33)])

    def test_parse_80(self):
        self.assertEqual(
            PAR.parse('reproductive data=scars R2, L2 ;'),
            [])

    def test_parse_81(self):
        self.assertEqual(
            PAR.parse('LENGTH 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN.'),
            [Parse(value=9.52, ambiguous_key=True, units='in',
                   start=0, end=13)])

    def test_parse_82(self):
        self.assertEqual(
            PAR.parse('LENGTH 0 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN.'),
            [Parse(value=9.52, ambiguous_key=True, units='in',
                   start=0, end=15)])

    def test_parse_83(self):
        self.assertEqual(
            PAR.parse('unformatted measurements=42-51 mm SL'),
            [Parse(value=[42, 51], units='mm', start=12, end=33)])

    def test_parse_84(self):
        self.assertEqual(
            PAR.parse('verbatim collector=R. D. Svihla 31-605 ; sex=male'),
            [])

    def test_parse_85(self):
        self.assertEqual(
            PAR.parse('Cataloged by: R.L. Humphrey, 31 January 1995'),
            [])

    def test_parse_86(self):
        self.assertEqual(
            PAR.parse(
                'measurement on tag for T. L. (141 mm) cannot be correct'),
            [Parse(value=141, units='mm', start=23, end=36)])

    def test_parse_87(self):
        self.assertEqual(
            PAR.parse('L: 275. T: 65.; '),
            [Parse(value=275, units_inferred=True, ambiguous_key=True,
                   start=0, end=6)])

    def test_parse_88(self):
        self.assertEqual(
            PAR.parse('unformatted measurements=L-11&#34;, T-3.125&#34;, '
                      'HF-1.5&#34; ; sex=male ; hind foot with claw=1.5 in; '
                      'total length=11 in; tail length=3.125 in   | .  '
                      '4/12/39 . | 1.5 TRUE'),
            [Parse(value=11, units_inferred=True, ambiguous_key=True,
                   start=25, end=29),
             Parse(value=279.4, units='in', units_inferred=False,
                   start=103, end=121)])

    def test_parse_89(self):
        self.assertEqual(
            PAR.parse('"relatedresourceid": '
                      '"99846657-2832-4987-94cd-451b9679725c"'),
            [])
