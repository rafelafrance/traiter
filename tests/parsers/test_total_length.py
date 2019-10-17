import unittest
from pylib.numeric_trait import NumericTrait
from pylib.parsers.total_length import TOTAL_LENGTH


class TestTotalLength(unittest.TestCase):

    def test_parse_001(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('{"totalLengthInMM":"123" };'),
            [NumericTrait(
                value=123, units_inferred=False, units='mm', start=2, end=23)])

    def test_parse_002(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                'measurements: ToL=230;TaL=115;HF=22;E=18;'
                ' total length=231 mm; tail length=115 mm;'),
            [NumericTrait(value=230, units=None, units_inferred=True,
                          start=14, end=21),
             NumericTrait(
                 value=231, units_inferred=False, units='mm',
                 start=42, end=61)])

    def test_parse_003(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                'measurements: ToL=230;TaL=115;HF=22;E=18;'
                ' total length=24 cm; tail length=115 mm;'),
            [NumericTrait(
                value=230, units=None, units_inferred=True, start=14, end=21),
             NumericTrait(
                 value=240, units_inferred=False, units='cm',
                 start=42, end=60)])

    def test_parse_004(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('sex=unknown ; crown-rump length=8 mm'),
            [])

    def test_parse_005(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                'left gonad length=10 mm; right gonad length=10 mm;'),
            [])

    def test_parse_006(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('"{"measurements":"308-190-45-20" }"'),
            [NumericTrait(
                value=308, units='mm_shorthand', units_inferred=False,
                is_shorthand=True, start=3, end=31)])

    def test_parse_007(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('308-190-45-20'),
            [NumericTrait(
                value=308, units='mm_shorthand', units_inferred=False,
                is_shorthand=True, start=0, end=13)])

    def test_parse_008(self):
        self.assertEqual(
            TOTAL_LENGTH.parse((
                'snout-vent length=54 mm; total length=111 mm;'
                ' tail length=57 mm; weight=5 g')),
            [NumericTrait(
                value=54, units='mm', units_inferred=False,
                start=0, end=23),
             NumericTrait(
                 value=111, units='mm', units_inferred=False,
                 start=25, end=44)])

    def test_parse_009(self):
        self.assertEqual(
            TOTAL_LENGTH.parse((
                'unformatted measurements=Verbatim weight=X;'
                'ToL=230;TaL=115;HF=22;E=18;'
                ' total length=231 mm; tail length=115 mm;')),
            [NumericTrait(
                value=230, units=None, units_inferred=True, start=43, end=50),
             NumericTrait(
                 value=231, units='mm', units_inferred=False,
                 start=71, end=90)])

    def test_parse_010(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('143-63-20-17=13'),
            [NumericTrait(
                value=143, units='mm_shorthand', units_inferred=False,
                is_shorthand=True, start=0, end=15)])

    def test_parse_011(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('** Body length =345 cm; Blubber=1 cm '),
            [NumericTrait(
                value=3450, units='cm', units_inferred=False,
                start=3, end=22)])

    def test_parse_012(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('t.l.= 2 feet 3.1 - 4.5 inches '),
            [NumericTrait(
                value=[688.34, 723.9], units=['ft', 'in'],
                units_inferred=False, start=0, end=29)])

    def test_parse_013(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('2 ft. 3.1 - 4.5 in. '),
            [NumericTrait(
                value=[688.34, 723.9], ambiguous_key=True,
                units=['ft', 'in'], units_inferred=False, start=0, end=18)])

    def test_parse_014(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('total length= 2 ft.'),
            [NumericTrait(
                value=609.6, units_inferred=False, units='ft',
                start=0, end=18)])

    def test_parse_015(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('AJR-32   186-102-23-15  15.0g'),
            [NumericTrait(
                value=186, units='mm_shorthand', units_inferred=False,
                is_shorthand=True, start=9, end=29)])

    def test_parse_016(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('length=8 mm'),
            [NumericTrait(
                value=8, units='mm', units_inferred=False, ambiguous_key=True,
                start=0, end=11)])

    def test_parse_017(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('another; length=8 mm'),
            [NumericTrait(
                value=8, units='mm', units_inferred=False, ambiguous_key=True,
                start=9, end=20)])

    def test_parse_018(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('another; TL_120, noise'),
            [NumericTrait(
                value=120, units=None, units_inferred=True, start=9, end=15)])

    def test_parse_019(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('another; TL - 101.3mm, noise'),
            [NumericTrait(
                value=101.3, units='mm', units_inferred=False,
                start=9, end=21)])

    def test_parse_020(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('before; TL153, after'),
            [NumericTrait(
                value=153, units=None, units_inferred=True, start=8, end=13)])

    def test_parse_021(self):
        self.assertEqual(
            TOTAL_LENGTH.parse((
                'before; Total length in catalog and '
                'specimen tag as 117, after')),
            [])

    def test_parse_022(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                'before Snout vent lengths range from 16 to 23 mm. qq'),
            [NumericTrait(
                value=[16, 23], units='mm', units_inferred=False,
                start=7, end=48)])

    def test_parse_023(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('Size=13 cm TL'),
            [NumericTrait(value=130, units='cm', units_inferred=False,
                          start=5, end=13)])

    def test_parse_024(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('det_comments:31.5-58.3inTL'),
            [NumericTrait(
                value=[800.1, 1480.82], units='in', units_inferred=False,
                start=13, end=26)])

    def test_parse_025(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('SVL52mm'),
            [NumericTrait(
                value=52, units='mm', units_inferred=False, start=0, end=7)])

    def test_parse_026(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                'snout-vent length=221 mm; total length=257 mm; '
                'tail length=36 mm'),
            [NumericTrait(
                value=221, units='mm', units_inferred=False, start=0, end=24),
             NumericTrait(
                 value=257, units='mm', units_inferred=False,
                 start=26, end=45)])

    def test_parse_027(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('SVL 209 mm, total 272 mm, 4.4 g.'),
            [NumericTrait(
                value=209, units='mm', units_inferred=False, start=0, end=10),
             NumericTrait(
                 value=272, units='mm', units_inferred=False,
                 start=12, end=24)])

    def test_parse_028(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                '{"time collected":"0712-0900", "length":"12.0" }'),
            [NumericTrait(
                value=12, ambiguous_key=True, units=None, units_inferred=True,
                start=32, end=45)])

    def test_parse_029(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                '{"time collected":"1030", "water depth":"1-8", '
                '"bottom":"abrupt lava cliff dropping off to sand at '
                '45 ft.", "length":"119-137" }'),
            [NumericTrait(
                value=[119, 137], ambiguous_key=True,
                units=None, units_inferred=True, start=109, end=125)])

    def test_parse_030(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx'),
            [NumericTrait(
                value=44, units='mm', units_inferred=False, start=0, end=10),
             NumericTrait(
                 value=38, units='mm', units_inferred=False,
                 start=11, end=21)])

    def test_parse_031(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('{"totalLengthInMM":"270-165-18-22-31", '),
            [NumericTrait(
                value=270, units='mm_shorthand', units_inferred=False,
                is_shorthand=True, start=20, end=36)])

    def test_parse_032(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('{"length":"20-29" }'),
            [NumericTrait(
                value=[20, 29], ambiguous_key=True,
                units=None, units_inferred=True,
                start=2, end=16)])

    def test_parse_033(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                'field measurements on fresh dead specimen were '
                '157-60-20-19-21g'),
            [NumericTrait(
                value=157, units='mm_shorthand', units_inferred=False,
                is_shorthand=True, start=47, end=63)])

    def test_parse_034(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                'f age class: adult; standard length: 63-107mm'),
            [NumericTrait(
                value=[63, 107], units='mm', units_inferred=False,
                start=20, end=45)])

    def test_parse_035(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('Rehydrated in acetic acid 7/1978-8/1987.'),
            [])

    def test_parse_036(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                'age class: adult; standard length: 18.0-21.5mm'),
            [NumericTrait(
                value=[18, 21.5], units='mm', units_inferred=False,
                start=18, end=46)])

    def test_parse_037(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('age class: adult; standard length: 18-21.5mm'),
            [NumericTrait(
                value=[18, 21.5], units='mm', units_inferred=False,
                start=18, end=44)])

    def test_parse_038(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('age class: adult; standard length: 18.0-21mm'),
            [NumericTrait(
                value=[18, 21], units='mm', units_inferred=False,
                start=18, end=44)])

    def test_parse_039(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('age class: adult; standard length: 18-21mm'),
            [NumericTrait(
                value=[18, 21], units='mm', units_inferred=False,
                start=18, end=42)])

    def test_parse_040(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                "Specimen #'s - 5491,5492,5498,5499,5505,5526,5527,5528,5500,"
                "5507,5508,5590,5592,5595,5594,5593,5596,5589,5587,5586,5585"),
            [])

    def test_parse_041(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('20-28mm SL'),
            [NumericTrait(
                value=[20, 28], units='mm', units_inferred=False,
                start=0, end=10)])

    def test_parse_042(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('29mm SL'),
            [NumericTrait(
                value=29, units='mm', units_inferred=False, start=0, end=7)])

    def test_parse_043(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('{"measurements":"159-?-22-16=21.0" }'),
            [NumericTrait(
                value=159, units='mm_shorthand', units_inferred=False,
                is_shorthand=True, start=2, end=33)])

    def test_parse_044(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('c701563b-dbd9-4500-184f-1ad61eb8da11'),
            [])

    def test_parse_045(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('Meas: L: 21.0'),
            [NumericTrait(
                value=21, units=None, units_inferred=True, start=0, end=13)])

    def test_parse_046(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('Meas: L: 21.0 cm'),
            [NumericTrait(
                value=210, units='cm', units_inferred=False, start=0, end=16)])

    def test_parse_047(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('LABEL. LENGTH 375 MM.'),
            [NumericTrait(
                value=375, units='mm', units_inferred=False, start=0, end=20)])

    def test_parse_048(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('SL=12mm'),
            [NumericTrait(
                value=12, units='mm', units_inferred=False, start=0, end=7)])

    def test_parse_049(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('Size=SL 12-14 mm'),
            [NumericTrait(
                value=[12, 14], units='mm', units_inferred=False,
                start=5, end=16)])

    def test_parse_050(self):
        self.assertEqual(TOTAL_LENGTH.parse('SV 1.2'), [])

    def test_parse_051(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(' Length: 123 mm SL'),
            [NumericTrait(
                value=123, units='mm', units_inferred=False, start=1, end=18)])

    def test_parse_052(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(' Length: 12-34 mmSL'),
            [NumericTrait(
                value=[12, 34], units='mm', units_inferred=False,
                start=1, end=19)])

    def test_parse_053(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('Measurements: L: 21.0 cm'),
            [NumericTrait(
                value=210, units='cm', units_inferred=False, start=0, end=24)])

    def test_parse_054(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('SVL=44'),
            [NumericTrait(
                value=44, units=None, units_inferred=True, start=0, end=6)])

    def test_parse_055(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('SVL=0 g'),
            [NumericTrait(
                value=0, units=None, units_inferred=True, start=0, end=5)])

    def test_parse_056(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('SVL=44'),
            [NumericTrait(
                value=44, units=None, units_inferred=True, start=0, end=6)])

    def test_parse_057(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('TL=50'),
            [NumericTrait(
                value=50, units=None, units_inferred=True, start=0, end=5)])

    def test_parse_058(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('SVL=44mm'),
            [NumericTrait(
                value=44, units='mm', units_inferred=False, start=0, end=8)])

    def test_parse_059(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('SV 1.4, TAIL 1.0 CM. HATCHLING'),
            [])

    def test_parse_060(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                'LENGTH 10 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN.'),
            [NumericTrait(
                value=263.52, ambiguous_key=True, units='in',
                units_inferred=False, start=0, end=16)])

    def test_parse_061(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                ('tail length in mm: -; total length in mm: -; '
                 'wing chord in mm: 81.0R; wing spread in mm: -')),
            [])

    def test_parse_062(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('76 cm S.L., 4.7 kg'),
            [NumericTrait(
                value=760, units='cm', units_inferred=False, start=0, end=10)])

    def test_parse_063(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('set mark: 661 1-5 64-61'),
            [])

    def test_parse_064(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('{"totalLength":"970", "wing":"390" }'),
            [NumericTrait(
                value=970, units=None, units_inferred=True, start=2, end=19)])

    def test_parse_065(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                'LENGTH: 117MM. SOFT self.parserTS COLOR ON LABEL.'),
            [NumericTrait(
                value=117, units='mm', units_inferred=False,
                ambiguous_key=True, start=0, end=13)])

    def test_parse_066(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('Meas:Length (L): 5'),
            [NumericTrait(
                value=5, units=None, units_inferred=True, start=0, end=18)])

    def test_parse_067(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('Size=41-148mm SL'),
            [NumericTrait(
                value=[41, 148], units='mm', units_inferred=False,
                start=5, end=16)])

    def test_parse_068(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('Size=105 mm TL, 87.1 mm PCL'),
            [NumericTrait(
                value=105, units='mm', units_inferred=False, start=5, end=14)])

    def test_parse_069(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('Total Length: 185-252 mm'),
            [NumericTrait(
                value=[185, 252], units='mm', units_inferred=False,
                start=0, end=24)])

    def test_parse_070(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('Total Length: 185 - 252 mm'),
            [NumericTrait(
                value=[185, 252], units='mm', units_inferred=False,
                start=0, end=26)])

    def test_parse_071(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('"bottom":"rock?", "length":"278" }'),
            [NumericTrait(
                value=278, ambiguous_key=True, units=None, units_inferred=True,
                start=19, end=31)])

    def test_parse_072(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('[308]-190-45-20'),
            [NumericTrait(
                value=308, units='mm_shorthand', units_inferred=False,
                is_shorthand=True, estimated_value=True, start=0, end=15)])

    def test_parse_073(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('"{"measurements":"[308]-190-45-20" }"'),
            [NumericTrait(
                value=308, units='mm_shorthand', units_inferred=False,
                is_shorthand=True, estimated_value=True, start=3, end=33)])

    def test_parse_074(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('308-190-45-20-11-22'),
            [])

    def test_parse_075(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('10 12/07/1944'),
            [])

    def test_parse_076(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('12-07-1944'),
            [])

    def test_parse_077(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('{"measurements":"210-92-30" }'),
            [NumericTrait(
                value=210, units='mm_shorthand', units_inferred=False,
                is_shorthand=True, start=2, end=26)])

    def test_parse_078(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('measurements:210-92-30 308-190-45-20'),
            [NumericTrait(
                value=308, units='mm_shorthand', units_inferred=False,
                is_shorthand=True, start=23, end=36)])

    def test_parse_079(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('measurements:210-92-30 185-252 mm'),
            [NumericTrait(
                value=[185, 252], units='mm', units_inferred=False,
                start=0, end=33)])

    def test_parse_080(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('reproductive data=scars R2, L2 ;'),
            [])

    def test_parse_081(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                'LENGTH 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN.'),
            [NumericTrait(
                value=9.52, ambiguous_key=True, units='in',
                units_inferred=False, start=0, end=13)])

    def test_parse_082(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                'LENGTH 0 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN.'),
            [NumericTrait(
                value=9.52, ambiguous_key=True, units='in',
                units_inferred=False, start=0, end=15)])

    def test_parse_083(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('unformatted measurements=42-51 mm SL'),
            [NumericTrait(
                value=[42, 51], units='mm', units_inferred=False,
                start=12, end=33)])

    def test_parse_084(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                'verbatim collector=R. D. Svihla 31-605 ; sex=male'),
            [])

    def test_parse_085(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('Cataloged by: R.L. Humphrey, 31 January 1995'),
            [])

    def test_parse_086(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                'measurement on tag for T. L. (141 mm) cannot be correct'),
            [NumericTrait(
                value=141, units='mm', units_inferred=False,
                start=23, end=36)])

    def test_parse_087(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('L: 275. T: 65.; '),
            [NumericTrait(
                value=275, units=None, units_inferred=True, ambiguous_key=True,
                start=0, end=6)])

    def test_parse_088(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                'unformatted measurements=L-11&#34;, T-3.125&#34;, '
                'HF-1.5&#34; ; sex=male ; hind foot with claw=1.5 in; '
                'total length=11 in; tail length=3.125 in   | .  '
                '4/12/39 . | 1.5 TRUE'),
            [NumericTrait(
                value=11, units=None, units_inferred=True, ambiguous_key=True,
                start=25, end=29),
             NumericTrait(
                 value=279.4, units='in', units_inferred=False,
                 start=103, end=121)])

    def test_parse_089(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                '"relatedresourceid": "99846657-2832-4987-94cd-451b9679725c"'),
            [])

    def test_parse_090(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                '{"created": "2014-10-29", "relatedresourceid": '
                '"eeba8b10-040e-4477-a0a6-870102b56234;'
                'abbf14f5-1a7c-48f6-8f2f-2a8af53c8c86"}'),
            [])

    def test_parse_091(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                '{"created": "2007-05-27", "relatedresourceid": '
                '"92bc5a20-577e-4504-aab6-bb409d06871a;'
                '0460ccc4-a461-43ec-86b6-1c252377b126"}'),
            [])

    def test_parse_092(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                '{"created": "2014-10-29", "relatedresourceid": '
                '"57d3efd8-2b9c-4952-8976-e27401a01251;'
                '8a35be5e-27fb-4875-81f6-42a5d7787760"}'),
            [])

    def test_parse_093(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('{"measurements":"TL=216.4 cm (+ 5 cm)" }'),
            [NumericTrait(
                value=2164, units='cm', units_inferred=False,
                start=17, end=28)])

    def test_parse_094(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('t.l.= 2 feet, 4.5 inches '),
            [NumericTrait(
                value=723.9, units=['ft', 'in'], units_inferred=False,
                start=0, end=24)])

    def test_parse_095(self):
        target = ('The length reported (2560 cm = 85 feet) is a bit '
                  'large for B. physalus and is more in keeping with B. '
                  'musculus. Redman, N. (2014). Whales\' Bones of France, '
                  'Southern Europe, Middle East and North Africa. '
                  'Teddington, England, Redman Publishing. '
                  'p. 24-25, 41-42')
        self.assertEqual(TOTAL_LENGTH.parse(target), [])

    def test_parse_096(self):
        self.assertEqual(TOTAL_LENGTH.parse('ELEV;1100 FT / 1500 FT?'), [])

    def test_parse_097(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                'This belongs with individual smaller than '
                'comparative specimen #4700 in 80-90 cmbd'),
            [])

    def test_parse_098(self):
        self.assertEqual(TOTAL_LENGTH.parse('ELEV;7500 FT=6700 FT'), [])

    def test_parse_099(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                '{"measurements":"TL=225 cm (265cm est) flukes cutoff", '
                '"weightInGrams":"299000.0" }'),
            [NumericTrait(
                value=2250, units='cm', units_inferred=False,
                start=17, end=26)])

    def test_parse_100(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                '{"measurements":"Weight=56700 TotalLength=1260 Tail=810 '
                'HindFoot=470" }'),
            [NumericTrait(
                value=1260, units=None, units_inferred=True,
                start=30, end=46)])

    def test_parse_101(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                'VERY YOUNG. LAST SPECIMEN CATALOGUED IN 1997.'),
            [])

    def test_parse_102(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                '{"measurements":"Weight=42700 TotalLength=1487.5 '
                'HindFoot=400" }'),
            [NumericTrait(
                value=1487.5, units=None, units_inferred=True,
                start=30, end=48)])

    def test_parse_103(self):
        self.assertEqual(
            TOTAL_LENGTH.parse(
                'Tail=239.0 mm; Hind Foot=74.0 mm (81.0 mm); Ear=34.0 mm.; '
                'Weight=560 g; Length=522.0 mm'),
            [NumericTrait(
                value=522, units='mm', units_inferred=False,
                ambiguous_key=True, start=72, end=87)])

    def test_parse_104(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('; trap identifier=SV01 S29/40 ;'),
            [])

    def test_parse_105(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('vagina opened; 4 embryos, R=3, L=1, CRL=28mm'),
            [])

    def test_parse_106(self):
        self.assertEqual(
            TOTAL_LENGTH.parse('trap TL01  26g; 212-115-27-20=26g;'),
            [NumericTrait(
                value=212, units='mm_shorthand', units_inferred=False,
                is_shorthand=True, start=16, end=33)])
