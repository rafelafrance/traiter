# pylint: disable=missing-docstring,too-many-public-methods

import unittest
from lib.parse import Parse
from lib.traits.body_mass_trait import BodyMassTrait


PAR = BodyMassTrait()


class TestBodyMassTrait(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('762-292-121-76 2435.0g'),
            [Parse(value=2435, units='g', start=0, end=22)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx'),
            [Parse(value=0.77, units='g', start=22, end=37)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse(
                'Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-62g'),
            [Parse(value=62, units='g', start=41, end=55)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('body mass=20 g'),
            [Parse(value=20, units='g', start=0, end=14)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('2 lbs. 3.1 - 4.5 oz '),
            [Parse(
                value=[995.07, 1034.76],
                ambiguous_key=True,
                units=['lbs', 'ozs'],
                start=0, end=19)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('{"totalLengthInMM":"x", "earLengthInMM":"20", '
                      '"weight":"[139.5] g" }'),
            [Parse(value=139.5, units='g', estimated_value=True,
                   start=47, end=65)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('{"fat":"No fat", "gonads":"Testes 10 x 6 mm.", '
                      '"molt":"No molt",'
                      ' "stomach contents":"Not recorded", "weight":"94 gr."'),
            [Parse(value=94, units='gr', start=101, end=115)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('Note in catalog: 83-0-17-23-fa64-35g'),
            [Parse(value=35, units='g', start=8, end=36)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('{"measurements":"20.2g, SVL 89.13mm" }'),
            [Parse(value=20.2, units='g', start=2, end=22)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('Body: 15 g'),
            [Parse(value=15, units='g', start=0, end=10)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('82-00-15-21-tr7-fa63-41g'),
            [Parse(value=41, units='g', start=0, end=24)])

    def test_parse_12(self):
        self.assertEqual(
            PAR.parse('weight=5.4 g; unformatted measurements=77-30-7-12=5.4'),
            [Parse(value=5.4, units='g', start=0, end=12),
             Parse(value=5.4, units_inferred=True,
                   start=26, end=53)])

    def test_parse_13(self):
        self.assertEqual(
            PAR.parse('unformatted measurements=77-30-7-12=5.4; weight=5.4;'),
            [Parse(value=5.4, units_inferred=True,
                   start=12, end=39),
             Parse(value=5.4, units_inferred=True,
                   start=41, end=51)])

    def test_parse_14(self):
        self.assertEqual(
            PAR.parse('{"totalLengthInMM":"270-165-18-22-31", '),
            [Parse(
                value=31,
                units_inferred=True,
                start=20, end=36)])

    def test_parse_15(self):
        self.assertEqual(
            PAR.parse('{"measurements":"143-63-20-17=13 g" }'),
            [Parse(value=13, units='g', start=2, end=34)])

    def test_parse_16(self):
        self.assertEqual(
            PAR.parse('143-63-20-17=13'),
            [Parse(value=13, units_inferred=True,
                   start=0, end=15)])

    def test_parse_17(self):
        self.assertEqual(
            PAR.parse('reproductive data: Testes descended -10x7 mm; sex: '
                      'male; unformatted measurements: 181-75-21-18=22 g'),
            [Parse(value=22, units='g', start=69, end=100)])

    def test_parse_18(self):
        self.assertEqual(
            PAR.parse('{ "massingrams"="20.1" }'),
            [Parse(value=20.1, units='grams', start=3, end=21)])

    def test_parse_19(self):
        self.assertEqual(
            PAR.parse(' {"gonadLengthInMM_1":"10", "gonadLengthInMM_2":"6", '
                      '"weight":"1,192.0" }'),
            [Parse(value=1192, units_inferred=True,
                   start=54, end=70)])

    def test_parse_20(self):
        self.assertEqual(
            PAR.parse('"weight: 20.5-31.8'),
            [Parse(value=[20.5, 31.8], units_inferred=True,
                   start=1, end=18)])

    def test_parse_21(self):
        self.assertEqual(
            PAR.parse('"weight: 20.5-32'),
            [Parse(value=[20.5, 32], units_inferred=True,
                   start=1, end=16)])

    def test_parse_22(self):
        self.assertEqual(
            PAR.parse('"weight: 21-31.8'),
            [Parse(
                value=[21, 31.8],
                units_inferred=True,
                start=1, end=16)])

    def test_parse_23(self):
        self.assertEqual(
            PAR.parse('"weight: 21-32'),
            [Parse(value=[21, 32], units_inferred=True,
                   start=1, end=14)])

    def test_parse_24(self):
        self.assertEqual(
            PAR.parse("Specimen #'s - 5491,5492,5498,5499,5505,5526,5527,"
                      "5528,5500,5507,5508,5590,5592,5595,5594,5593,5596,"
                      "5589,5587,5586,5585"),
            [])

    def test_parse_25(self):
        self.assertEqual(
            PAR.parse('weight=5.4 g; unformatted measurements=77-x-7-12=5.4'),
            [Parse(value=5.4, units='g', start=0, end=12),
             Parse(value=5.4, units_inferred=True,
                   start=26, end=52)])

    def test_parse_26(self):
        self.assertEqual(
            PAR.parse('c701563b-dbd9-4500-184f-1ad61eb8da11'),
            [])

    def test_parse_27(self):
        self.assertEqual(
            PAR.parse('body mass=0 g'),
            [Parse(value=0, units='g', start=0, end=13)])

    def test_parse_28(self):
        self.assertEqual(
            PAR.parse('2 lbs. 3.1 oz '),
            [Parse(value=995.07, ambiguous_key=True,
                   units=['lbs', 'ozs'], start=0, end=13)])

    def test_parse_29(self):
        self.assertEqual(
            PAR.parse(
                'Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-[62]g'),
            [Parse(value=62, units='g', estimated_value=True,
                   start=41, end=57)])

    def test_parse_30(self):
        self.assertEqual(
            PAR.parse(
                'Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-[62g]'),
            [Parse(value=62, units='g', estimated_value=True,
                   start=41, end=57)])

    def test_parse_31(self):
        self.maxDiff = None
        self.assertEqual(
            PAR.parse(
                'Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-[62] x'),
            [Parse(value=62,
                   estimated_value=True, units_inferred=True,
                   start=41, end=56)])

    def test_parse_32(self):
        self.assertEqual(
            PAR.parse('wt=10 g'),
            [Parse(value=10, units='g', start=0, end=7)])

    def test_parse_33(self):
        self.assertEqual(
            PAR.parse('w.t.=10 g'),
            [Parse(value=10, units='g', start=0, end=9)])

    def test_parse_34(self):
        self.assertEqual(
            PAR.parse('DATA HISTORY: Inventory catalogued/verified by '
                      'Collections staff (2008-2010 inventory). Record last '
                      'updated in Excel (prior to Arctos migration) by Dawn '
                      'R. Roberts (2013-11-30). Date listed as entered in '
                      'original FileMaker database: 1988-07-29.'),
            [])

    def test_parse_35(self):
        self.assertEqual(
            PAR.parse('; weight = [50.8] g ;'),
            [Parse(value=50.8, units='g', estimated_value=True,
                   start=2, end=19)])

    def test_parse_36(self):
        self.assertEqual(
            PAR.parse('{"measurements":"242-109-37-34=N/D" }'),
            [])
