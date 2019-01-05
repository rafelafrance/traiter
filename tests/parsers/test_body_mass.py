# flake8=noqa

import unittest
from lib.parsers.base import Result
from lib.parsers.body_mass import BodyMass


PAR = BodyMass()


class TestBodyMass(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('762-292-121-76 2435.0g'),
            [Result(value=2435.0, units='g', start=0, end=22)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx'),
            [Result(value=0.77, units='g', start=22, end=37)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse(
                'Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-62g'),
            [Result(value=62, units='g', start=41, end=55)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('body mass=20 g'),
            [Result(value=20, units='g', start=0, end=14)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('2 lbs. 3.1 - 4.5 oz '),
            [Result(value=[995.07, 1034.76],
                    ambiguous=True,
                    units=['lbs', 'oz'],
                    start=0, end=19)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('{"totalLengthInMM":"x", "earLengthInMM":"20", '
                      '"weight":"[139.5] g" }'),
            [Result(value=139.5, units='g', start=47, end=65)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('{"fat":"No fat", "gonads":"Testes 10 x 6 mm.", '
                      '"molt":"No molt",'
                      ' "stomach contents":"Not recorded", "weight":"94 gr."'),
            [Result(value=94, units='gr', start=101, end=115)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('Note in catalog: 83-0-17-23-fa64-35g'),
            [Result(value=35, units='g', start=8, end=36)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('{"measurements":"20.2g, SVL 89.13mm" }'),
            [Result(value=20.2, units='g', start=2, end=22)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('Body: 15 g'),
            [Result(value=15, units='g', start=0, end=10)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('82-00-15-21-tr7-fa63-41g'),
            [Result(value=41, units='g', start=0, end=24)])

    def test_parse_12(self):
        self.assertEqual(
            PAR.parse('weight=5.4 g; unformatted measurements=77-30-7-12=5.4'),
            [Result(value=5.4, units='g', start=0, end=12),
             Result(value=5.4, units=None, start=26, end=53)])

    def test_parse_13(self):
        self.assertEqual(
            PAR.parse('unformatted measurements=77-30-7-12=5.4; weight=5.4;'),
            [Result(value=5.4, units=None, start=12, end=39),
             Result(value=5.4, units=None, start=41, end=51)])

    def test_parse_14(self):
        self.assertEqual(
            PAR.parse('{"totalLengthInMM":"270-165-18-22-31", '),
            [Result(value=31, units=None, start=20, end=36)])

    def test_parse_15(self):
        self.assertEqual(
            PAR.parse('{"measurements":"143-63-20-17=13 g" }'),
            [Result(value=13, units='g', start=2, end=34)])

    def test_parse_16(self):
        self.assertEqual(
            PAR.parse('143-63-20-17=13'),
            [Result(value=13, units=None, start=0, end=15)])

    def test_parse_17(self):
        self.assertEqual(
            PAR.parse('reproductive data: Testes descended -10x7 mm; sex: '
                      'male; unformatted measurements: 181-75-21-18=22 g'),
            [Result(value=22, units='g', start=69, end=100)])

    def test_parse_18(self):
        self.assertEqual(
            PAR.parse('{ "massingrams"="20.1" }'),
            [Result(value=20.1, units='massingrams', start=3, end=21)])

    def test_parse_19(self):
        self.assertEqual(
            PAR.parse(' {"gonadLengthInMM_1":"10", "gonadLengthInMM_2":"6", '
                      '"weight":"1,192.0" }'),
            [Result(value=1192.0, units=None, start=54, end=70)])

    def test_parse_20(self):
        self.assertEqual(
            PAR.parse('"weight: 20.5-31.8'),
            [Result(value=[20.5, 31.8], units=None, start=1, end=18)])

    def test_parse_21(self):
        self.assertEqual(
            PAR.parse('"weight: 20.5-32'),
            [Result(value=[20.5, 32], units=None, start=1, end=16)])

    def test_parse_22(self):
        self.assertEqual(
            PAR.parse('"weight: 21-31.8'),
            [Result(value=[21, 31.8], units=None, start=1, end=16)])

    def test_parse_23(self):
        self.assertEqual(
            PAR.parse('"weight: 21-32'),
            [Result(value=[21, 32], units=None, start=1, end=14)])

    def test_parse_24(self):
        self.assertEqual(
            PAR.parse("Specimen #'s - 5491,5492,5498,5499,5505,5526,5527,"
                      "5528,5500,5507,5508,5590,5592,5595,5594,5593,5596,"
                      "5589,5587,5586,5585"),
            [])

    def test_parse_26(self):
        self.assertEqual(
            PAR.parse('weight=5.4 g; unformatted measurements=77-x-7-12=5.4'),
            [Result(value=5.4, units='g', start=0, end=12),
             Result(value=5.4, units=None, start=26, end=52)])

    def test_parse_27(self):
        self.assertEqual(
            PAR.parse('c701563b-dbd9-4500-184f-1ad61eb8da11'),
            [])

    def test_parse_28(self):
        self.assertEqual(
            PAR.parse('body mass=0 g'),
            [Result(value=0.0, units='g', start=0, end=13)])

    def test_parse_29(self):
        self.assertEqual(
            PAR.parse('2 lbs. 3.1 oz '),
            [Result(value=995.07, ambiguous=True, units=['lbs', 'oz'],
                    start=0, end=13)])
