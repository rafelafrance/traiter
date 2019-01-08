# flake8=noqa

import unittest
from lib.result import Result
from lib.traits.total_length import TotalLength


PAR = TotalLength()


class TestTotalLength(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('{"totalLengthInMM":"123" };'),
            [Result(value=123.0, units='totallengthinmm', start=2, end=23)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('measurements: ToL=230;TaL=115;HF=22;E=18;'
                      ' total length=231 mm; tail length=115 mm;'),
            [Result(value=230.0, flags={'units_inferred': True},
                    start=14, end=21),
             Result(value=231.0, units='mm', start=42, end=61)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('measurements: ToL=230;TaL=115;HF=22;E=18;'
                      ' total length=24 cm; tail length=115 mm;'),
            [Result(value=230.0, flags={'units_inferred': True},
                    start=14, end=21),
             Result(value=240.0, units='cm', start=42, end=60)])

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
            [Result(value=308.0, units='mm_shorthand', start=3, end=31)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('308-190-45-20'),
            [Result(value=308.0, units='mm_shorthand', start=0, end=13)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse((
                'snout-vent length=54 mm; total length=111 mm;'
                ' tail length=57 mm; weight=5 g')),
            [Result(value=54.0, units='mm', start=0, end=23),
             Result(value=111.0, units='mm', start=25, end=44)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse((
                'unformatted measurements=Verbatim weight=X;'
                'ToL=230;TaL=115;HF=22;E=18;'
                ' total length=231 mm; tail length=115 mm;')),
            [Result(value=230.0, flags={'units_inferred': True},
                    start=43, end=50),
             Result(value=231.0, units='mm', start=71, end=90)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('143-63-20-17=13'),
            [Result(value=143.0, units='mm_shorthand', start=0, end=15)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('** Body length =345 cm; Blubber=1 cm '),
            [Result(value=3450.0, units='cm', start=3, end=22)])

    def test_parse_12(self):
        self.assertEqual(
            PAR.parse('t.l.= 2 feet 3.1 - 4.5 inches '),
            [Result(value=[688.34, 723.9], units=['ft', 'in'],
                    start=0, end=29)])

    def test_parse_13(self):
        self.assertEqual(
            PAR.parse('2 ft. 3.1 - 4.5 in. '),
            [Result(value=[688.34, 723.9], flags={'ambiguous_key': True},
                    units=['ft', 'in'], start=0, end=18)])

    def test_parse_14(self):
        self.assertEqual(
            PAR.parse('total length= 2 ft.'),
            [Result(value=609.6, units='ft', start=0, end=18)])

    def test_parse_15(self):
        self.assertEqual(
            PAR.parse('AJR-32   186-102-23-15  15.0g'),
            [Result(value=186.0, units='mm_shorthand', start=9, end=29)])

    def test_parse_16(self):
        self.assertEqual(
            PAR.parse('length=8 mm'),
            [Result(value=8.0, units='mm', flags={'ambiguous_key': True},
                    start=0, end=11)])

    def test_parse_17(self):
        self.assertEqual(
            PAR.parse('another; length=8 mm'),
            [Result(value=8.0, units='mm', flags={'ambiguous_key': True},
                    start=9, end=20)])

    def test_parse_18(self):
        self.assertEqual(
            PAR.parse('another; TL_120, noise'),
            [Result(value=120.0, flags={'units_inferred': True},
                    start=9, end=15)])

    def test_parse_19(self):
        self.assertEqual(
            PAR.parse('another; TL - 101.3mm, noise'),
            [Result(value=101.3, units='mm', start=9, end=21)])

    def test_parse_20(self):
        self.assertEqual(
            PAR.parse('before; TL153, after'),
            [Result(value=153.0, flags={'units_inferred': True},
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
            [Result(value=[16.0, 23.0], units='mm', start=7, end=48)])

    def test_parse_23(self):
        self.assertEqual(
            PAR.parse('Size=13 cm TL'),
            [Result(value=130.0, units='cm', start=5, end=13)])

    def test_parse_24(self):
        self.assertEqual(
            PAR.parse('det_comments:31.5-58.3inTL'),
            [Result(value=[800.1, 1480.82], units='in', start=13, end=26)])

    def test_parse_25(self):
        self.assertEqual(
            PAR.parse('SVL52mm'),
            [Result(value=52, units='mm', start=0, end=7)])

    def test_parse_26(self):
        self.assertEqual(
            PAR.parse('snout-vent length=221 mm; total length=257 mm; '
                      'tail length=36 mm'),
            [Result(value=221, units='mm', start=0, end=24),
             Result(value=257, units='mm', start=26, end=45)])

    def test_parse_27(self):
        self.assertEqual(
            PAR.parse('SVL 209 mm, total 272 mm, 4.4 g.'),
            [Result(value=209.0, units='mm', start=0, end=10),
             Result(value=272.0, units='mm', start=12, end=24)])

    def test_parse_28(self):
        self.assertEqual(
            PAR.parse('{"time collected":"0712-0900", "length":"12.0" }'),
            [Result(value=12.0,
                    flags={'ambiguous_key': True, 'units_inferred': True},
                    start=32, end=45)])

    def test_parse_29(self):
        self.assertEqual(
            PAR.parse('{"time collected":"1030", "water depth":"1-8", '
                      '"bottom":"abrupt lava cliff dropping off to sand at '
                      '45 ft.", "length":"119-137" }'),
            [Result(value=[119.0, 137.0],
                    flags={'ambiguous_key': True, 'units_inferred': True},
                    start=109, end=125)])

    def test_parse_30(self):
        self.assertEqual(
            PAR.parse('TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx'),
            [Result(value=44, units='mm', start=0, end=10),
             Result(value=38, units='mm', start=11, end=21)])

    def test_parse_31(self):
        self.assertEqual(
            PAR.parse('{"totalLengthInMM":"270-165-18-22-31", '),
            [Result(value=270.0, units='mm_shorthand', start=20, end=36)])

    def test_parse_32(self):
        self.assertEqual(
            PAR.parse('{"length":"20-29" }'),
            [Result(value=[20, 29],
                    flags={'ambiguous_key': True, 'units_inferred': True},
                    start=2, end=16)])

    def test_parse_33(self):
        self.assertEqual(
            PAR.parse('field measurements on fresh dead specimen were '
                      '157-60-20-19-21g'),
            [Result(value=157, units='mm_shorthand', start=47, end=63)])

    def test_parse_34(self):
        self.assertEqual(
            PAR.parse('f age class: adult; standard length: 63-107mm'),
            [Result(value=[63, 107], units='mm', start=20, end=45)])

    def test_parse_35(self):
        self.assertEqual(
            PAR.parse('Rehydrated in acetic acid 7/1978-8/1987.'),
            [])

    def test_parse_36(self):
        self.assertEqual(
            PAR.parse('age class: adult; standard length: 18.0-21.5mm'),
            [Result(value=[18.0, 21.5], units='mm', start=18, end=46)])

    def test_parse_37(self):
        self.assertEqual(
            PAR.parse('age class: adult; standard length: 18-21.5mm'),
            [Result(value=[18, 21.5], units='mm', start=18, end=44)])

    def test_parse_38(self):
        self.assertEqual(
            PAR.parse('age class: adult; standard length: 18.0-21mm'),
            [Result(value=[18.0, 21], units='mm', start=18, end=44)])

    def test_parse_39(self):
        self.assertEqual(
            PAR.parse('age class: adult; standard length: 18-21mm'),
            [Result(value=[18, 21], units='mm', start=18, end=42)])

    def test_parse_40(self):
        self.assertEqual(
            PAR.parse(
                "Specimen #'s - 5491,5492,5498,5499,5505,5526,5527,5528,5500,"
                "5507,5508,5590,5592,5595,5594,5593,5596,5589,5587,5586,5585"),
            [])

    def test_parse_41(self):
        self.assertEqual(
            PAR.parse('20-28mm SL'),
            [Result(value=[20, 28], units='mm', start=0, end=10)])

    def test_parse_42(self):
        self.assertEqual(
            PAR.parse('29mm SL'),
            [Result(value=29, units='mm', start=0, end=7)])

    def test_parse_43(self):
        self.assertEqual(
            PAR.parse('{"measurements":"159-?-22-16=21.0" }'),
            [Result(value=159, units='mm_shorthand', start=2, end=33)])

    def test_parse_44(self):
        self.assertEqual(
            PAR.parse('c701563b-dbd9-4500-184f-1ad61eb8da11'),
            [])

    def test_parse_45(self):
        self.assertEqual(
            PAR.parse('Meas: L: 21.0'),
            [Result(value=21.0, flags={'units_inferred': True},
                    start=0, end=13)])

    def test_parse_46(self):
        self.assertEqual(
            PAR.parse('Meas: L: 21.0 cm'),
            [Result(value=210.0, units='cm', start=0, end=16)])

    def test_parse_47(self):
        self.assertEqual(
            PAR.parse('LABEL. LENGTH 375 MM.'),
            [Result(value=375, units='MM', start=0, end=20)])

    def test_parse_48(self):
        self.assertEqual(
            PAR.parse('SL=12mm'),
            [Result(value=12, units='mm', start=0, end=7)])

    def test_parse_49(self):
        self.assertEqual(
            PAR.parse('Size=SL 12-14 mm'),
            [Result(value=[12, 14], units='mm', start=5, end=16)])

    def test_parse_50(self):
        self.assertEqual(
            PAR.parse('SV 1.2'),
            [Result(value=1.2, flags={'units_inferred': True},
                    start=0, end=6)])

    def test_parse_51(self):
        self.assertEqual(
            PAR.parse(' Length: 123 mm SL'),
            [Result(value=123, units='mm', start=1, end=18)])

    def test_parse_52(self):
        self.assertEqual(
            PAR.parse(' Length: 12-34 mmSL'),
            [Result(value=[12, 34], units='mm', start=1, end=19)])

    def test_parse_53(self):
        self.assertEqual(
            PAR.parse('Measurements: L: 21.0 cm'),
            [Result(value=210.0, units='cm', start=0, end=24)])

    def test_parse_54(self):
        self.assertEqual(
            PAR.parse('SVL=44'),
            [Result(value=44, flags={'units_inferred': True},
                    start=0, end=6)])

    def test_parse_55(self):
        self.assertEqual(
            PAR.parse('SVL=0 g'),
            [Result(value=0.0, flags={'units_inferred': True},
                    start=0, end=5)])

    def test_parse_56(self):
        self.assertEqual(
            PAR.parse('SVL=44'),
            [Result(value=44, flags={'units_inferred': True},
                    start=0, end=6)])

    def test_parse_57(self):
        self.assertEqual(
            PAR.parse('TL=50'),
            [Result(value=50, flags={'units_inferred': True},
                    start=0, end=5)])

    def test_parse_58(self):
        self.assertEqual(
            PAR.parse('SVL=44mm'),
            [Result(value=44, units='mm', start=0, end=8)])

    def test_parse_58a(self):
        self.assertEqual(
            PAR.parse('unformatted measurements=42-51 mm SL'),
            [Result(value=[42, 51], units='mm', start=12, end=33)])

    def test_parse_59(self):
        # Infer the units from other measurements in post processing
        self.assertEqual(
            PAR.parse('SV 1.4, TAIL 1.0 CM. HATCHLING'),
            [Result(value=1.4, flags={'units_inferred': True},
                    start=0, end=6)])

    def test_parse_60(self):
        self.assertEqual(
            PAR.parse('LENGTH 10 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN.'),
            [Result(value=263.52, flags={'ambiguous_key': True}, units='in',
                    start=0, end=16)])

    def test_parse_60a(self):
        self.assertEqual(
            PAR.parse('LENGTH 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN.'),
            [Result(value=9.52, flags={'ambiguous_key': True}, units='in',
                    start=0, end=13)])

    def test_parse_60b(self):
        self.assertEqual(
            PAR.parse('LENGTH 0 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN.'),
            [Result(value=9.52, flags={'ambiguous_key': True}, units='in',
                    start=0, end=15)])

    def test_parse_61(self):
        self.assertEqual(
            PAR.parse(
                ('tail length in mm: -; total length in mm: -; '
                 'wing chord in mm: 81.0R; wing spread in mm: -')),
            [])

    def test_parse_62(self):
        self.assertEqual(
            PAR.parse('76 cm S.L., 4.7 kg'),
            [Result(value=760, units='cm', start=0, end=10)])

    def test_parse_63(self):
        self.assertEqual(
            PAR.parse('set mark: 661 1-5 64-61'),
            [])

    def test_parse_64(self):
        self.assertEqual(
            PAR.parse('{"totalLength":"970", "wing":"390" }'),
            [Result(value=970, flags={'units_inferred': True},
                    start=2, end=19)])

    def test_parse_65(self):
        self.assertEqual(
            PAR.parse('LENGTH: 117MM. SOFT PARTS COLOR ON LABEL.'),
            [Result(value=117, flags={'ambiguous_key': True}, units='MM',
                    start=0, end=13)])

    def test_parse_66(self):
        self.assertEqual(
            PAR.parse('Meas:Length (L): 5'),
            [Result(value=5, flags={'units_inferred': True},
                    start=0, end=18)])

    def test_parse_67(self):
        self.assertEqual(
            PAR.parse('Size=41-148mm SL'),
            [Result(value=[41, 148], units='mm', start=5, end=16)])

    def test_parse_68(self):
        self.assertEqual(
            PAR.parse('Size=105 mm TL, 87.1 mm PCL'),
            [Result(value=105, units='mm', start=5, end=14)])

    def test_parse_69(self):
        self.assertEqual(
            PAR.parse('Total Length: 185-252 mm'),
            [Result(value=[185, 252], units='mm', start=0, end=24)])

    def test_parse_70(self):
        self.assertEqual(
            PAR.parse('Total Length: 185 - 252 mm'),
            [Result(value=[185, 252], units='mm', start=0, end=26)])

    def test_parse_71(self):
        self.assertEqual(
            PAR.parse('"bottom":"rock?", "length":"278" }'),
            [Result(value=278,
                    flags={'ambiguous_key': True, 'units_inferred': True},
                    start=19, end=31)])

    def test_parse_72(self):
        self.assertEqual(
            PAR.parse('[308]-190-45-20'),
            [Result(value=308.0, units='mm_shorthand',
                    flags={'estimated_value': True},
                    start=1, end=15)])

    def test_parse_73(self):
        self.assertEqual(
            PAR.parse('"{"measurements":"[308]-190-45-20" }"'),
            [Result(value=308.0, units='mm_shorthand',
                    flags={'estimated_value': True},
                    start=3, end=33)])

    def test_parse_74(self):
        self.assertEqual(
            PAR.parse('308-190-45-20-11-22'),
            [])
