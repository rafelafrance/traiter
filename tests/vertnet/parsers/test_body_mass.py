# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods
import unittest
from pylib.vertnet.trait import Trait
from pylib.vertnet.parsers.body_mass import BODY_MASS


class TestBodyMass(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            BODY_MASS.parse('762-292-121-76 2435.0g'),
            [Trait(
                value=2435, units='g', units_inferred=False,
                is_shorthand=True, start=0, end=22)])

    def test_parse_02(self):
        self.assertEqual(
            BODY_MASS.parse('TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx'),
            [Trait(
                value=0.77, units='g', units_inferred=False,
                start=22, end=37)])

    def test_parse_03(self):
        self.assertEqual(
            BODY_MASS.parse(
                'Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-62g'),
            [Trait(
                value=62, units='g', units_inferred=False, is_shorthand=True,
                start=41, end=55)])

    def test_parse_04(self):
        self.assertEqual(
            BODY_MASS.parse('body mass=20 g'),
            [Trait(
                value=20, units='g', units_inferred=False, start=0, end=14)])

    def test_parse_05(self):
        self.assertEqual(
            BODY_MASS.parse('2 lbs. 3.1 - 4.5 oz '),
            [Trait(
                value=[995.06, 1034.75],
                ambiguous_key=True,
                units=['lbs', 'oz'],
                units_inferred=False,
                start=0, end=19)])

    def test_parse_06(self):
        self.assertEqual(
            BODY_MASS.parse(
                '{"totalLengthInMM":"x", "earLengthInMM":"20", '
                '"weight":"[139.5] g" }'),
            [Trait(
                value=139.5, units='g', units_inferred=False,
                estimated_value=True, start=47, end=65)])

    def test_parse_07(self):
        self.assertEqual(
            BODY_MASS.parse(
                '{"fat":"No fat", "gonads":"Testes 10 x 6 mm.", '
                '"molt":"No molt",'
                ' "stomach contents":"Not recorded", "weight":"94 gr."'),
            [Trait(
                value=94, units='gr', units_inferred=False,
                start=101, end=115)])

    def test_parse_08(self):
        self.assertEqual(
            BODY_MASS.parse('Note in catalog: 83-0-17-23-fa64-35g'),
            [Trait(
                value=35, units='g', units_inferred=False, is_shorthand=True,
                start=8, end=36)])

    def test_parse_09(self):
        self.assertEqual(
            BODY_MASS.parse('{"measurements":"20.2g, SVL 89.13mm" }'),
            [Trait(
                value=20.2, units='g', units_inferred=False, start=2, end=22)])

    def test_parse_10(self):
        self.assertEqual(
            BODY_MASS.parse('Body: 15 g'),
            [Trait(
                value=15, units='g', units_inferred=False, start=0, end=10)])

    def test_parse_11(self):
        self.assertEqual(
            BODY_MASS.parse('82-00-15-21-tr7-fa63-41g'),
            [Trait(
                value=41, units='g', units_inferred=False, is_shorthand=True,
                start=0, end=24)])

    def test_parse_12(self):
        self.assertEqual(
            BODY_MASS.parse(
                'weight=5.4 g; unformatted measurements=77-30-7-12=5.4'),
            [
                Trait(
                    value=5.4, units='g', units_inferred=False,
                    start=0, end=12),
                Trait(
                    value=5.4, units=None, units_inferred=True,
                    is_shorthand=True, start=26, end=53)])

    def test_parse_13(self):
        self.assertEqual(
            BODY_MASS.parse(
                'unformatted measurements=77-30-7-12=5.4; weight=5.4;'),
            [
                Trait(
                    value=5.4, units=None, units_inferred=True,
                    is_shorthand=True, start=12, end=39),
                Trait(
                    value=5.4, units=None, units_inferred=True,
                    start=41, end=51)])

    def test_parse_14(self):
        self.assertEqual(
            BODY_MASS.parse('{"totalLengthInMM":"270-165-18-22-31", '),
            [Trait(
                value=31, units=None, units_inferred=True, is_shorthand=True,
                start=20, end=36)])

    def test_parse_15(self):
        self.assertEqual(
            BODY_MASS.parse('{"measurements":"143-63-20-17=13 g" }'),
            [Trait(
                value=13, units='g', units_inferred=False, is_shorthand=True,
                start=2, end=34)])

    def test_parse_16(self):
        self.assertEqual(
            BODY_MASS.parse('143-63-20-17=13'),
            [Trait(
                value=13, units=None, units_inferred=True, is_shorthand=True,
                start=0, end=15)])

    def test_parse_17(self):
        self.assertEqual(
            BODY_MASS.parse(
                'reproductive data: Testes descended -10x7 mm; sex: '
                'male; unformatted measurements: 181-75-21-18=22 g'),
            [Trait(
                value=22, units='g', units_inferred=False, is_shorthand=True,
                start=69, end=100)])

    def test_parse_18(self):
        self.assertEqual(
            BODY_MASS.parse('{ "massingrams"="20.1" }'),
            [Trait(
                value=20.1, units='grams', units_inferred=False,
                start=3, end=21)])

    def test_parse_19(self):
        self.assertEqual(
            BODY_MASS.parse(
                ' {"gonadLengthInMM_1":"10", "gonadLengthInMM_2":"6", '
                '"weight":"1,192.0" }'),
            [Trait(
                value=1192, units=None, units_inferred=True,
                start=54, end=70)])

    def test_parse_20(self):
        self.assertEqual(
            BODY_MASS.parse('"weight: 20.5-31.8'),
            [Trait(
                value=[20.5, 31.8], units=None, units_inferred=True,
                start=1, end=18)])

    def test_parse_21(self):
        self.assertEqual(
            BODY_MASS.parse('"weight: 20.5-32'),
            [Trait(
                value=[20.5, 32], units=None, units_inferred=True,
                start=1, end=16)])

    def test_parse_22(self):
        self.assertEqual(
            BODY_MASS.parse('"weight: 21-31.8'),
            [Trait(
                value=[21, 31.8], units=None, units_inferred=True,
                start=1, end=16)])

    def test_parse_23(self):
        self.assertEqual(
            BODY_MASS.parse('"weight: 21-32'),
            [Trait(
                value=[21, 32], units=None, units_inferred=True,
                start=1, end=14)])

    def test_parse_24(self):
        self.assertEqual(
            BODY_MASS.parse(
                "Specimen #'s - 5491,5492,5498,5499,5505,5526,5527,"
                "5528,5500,5507,5508,5590,5592,5595,5594,5593,5596,"
                "5589,5587,5586,5585"),
            [])

    def test_parse_25(self):
        self.assertEqual(
            BODY_MASS.parse(
                'weight=5.4 g; unformatted measurements=77-x-7-12=5.4'),
            [
                Trait(
                    value=5.4, units='g', units_inferred=False,
                    start=0, end=12),
                Trait(
                    value=5.4, units=None, units_inferred=True,
                    is_shorthand=True, start=26, end=52)])

    def test_parse_26(self):
        self.assertEqual(
            BODY_MASS.parse('c701563b-dbd9-4500-184f-1ad61eb8da11'),
            [])

    def test_parse_27(self):
        self.assertEqual(
            BODY_MASS.parse('body mass=0 g'),
            [Trait(
                value=0, units='g', units_inferred=False, start=0, end=13)])

    def test_parse_28(self):
        self.assertEqual(
            BODY_MASS.parse('2 lbs. 3.1 oz '),
            [Trait(
                value=995.06, ambiguous_key=True,
                units=['lbs', 'oz'], units_inferred=False, start=0, end=13)])

    def test_parse_29(self):
        self.assertEqual(
            BODY_MASS.parse(
                'Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-[62]g'),
            [Trait(
                value=62, units='g', units_inferred=False, is_shorthand=True,
                estimated_value=True, start=41, end=57)])

    def test_parse_30(self):
        self.assertEqual(
            BODY_MASS.parse(
                'Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-[62g]'),
            [Trait(
                value=62, units='g', units_inferred=False, is_shorthand=True,
                estimated_value=True, start=41, end=57)])

    def test_parse_31(self):
        self.assertEqual(
            BODY_MASS.parse(
                'Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-[62] x'),
            [Trait(
                value=62, estimated_value=True, units=None,
                units_inferred=True, is_shorthand=True, start=41, end=56)])

    def test_parse_32(self):
        self.assertEqual(
            BODY_MASS.parse('wt=10 g'),
            [Trait(
                value=10, units='g', units_inferred=False, start=0, end=7)])

    def test_parse_33(self):
        self.assertEqual(
            BODY_MASS.parse('w.t.=10 g'),
            [Trait(
                value=10, units='g', units_inferred=False, start=0, end=9)])

    def test_parse_34(self):
        self.assertEqual(
            BODY_MASS.parse(
                'DATA HISTORY: Inventory catalogued/verified by '
                'Collections staff (2008-2010 inventory). Record last '
                'updated in Excel (prior to Arctos migration) by Dawn '
                'R. Roberts (2013-11-30). Date listed as entered in '
                'original FileMaker database: 1988-07-29.'),
            [])

    def test_parse_35(self):
        self.assertEqual(
            BODY_MASS.parse('; weight = [50.8] g ;'),
            [Trait(
                value=50.8, units='g', units_inferred=False,
                estimated_value=True, start=2, end=19)])

    def test_parse_36(self):
        self.assertEqual(
            BODY_MASS.parse('{"measurements":"242-109-37-34=N/D" }'),
            [])

    def test_parse_37(self):
        self.assertEqual(
            BODY_MASS.parse(
                'ear from notch=9 mm; weight=.65 kg; reproductive data'),
            [Trait(
                value=650, units='kg', units_inferred=False,
                start=21, end=34)])

    def test_parse_38(self):
        self.assertEqual(
            BODY_MASS.parse('; weight=22 oz; Verbatim weight=1lb 6oz;'),
            [
                Trait(
                    value=623.69, units='oz', units_inferred=False,
                    start=2, end=14),
                Trait(
                    value=623.69, units=['lb', 'oz'], units_inferred=False,
                    start=25, end=39)])

    def test_parse_39(self):
        self.assertEqual(
            BODY_MASS.parse('bacu wt=0.09'),
            [])

    def test_parse_40(self):
        self.assertEqual(
            BODY_MASS.parse('femur wt=1.05'),
            [])

    def test_parse_41(self):
        self.assertEqual(
            BODY_MASS.parse(
                '{"created": "2014-10-29", "relatedresourceid": '
                '"eeba8b10-040e-4477-a0a6-870102b56234;'
                'abbf14f5-1a7c-48f6-8f2f-2a8af53c8c86"}'),
            [])

    def test_parse_42(self):
        self.assertEqual(
            BODY_MASS.parse(
                '{"created": "2007-05-27", "relatedresourceid": '
                '"92bc5a20-577e-4504-aab6-bb409d06871a;'
                '0460ccc4-a461-43ec-86b6-1c252377b126"}'),
            [])

    def test_parse_43(self):
        self.assertEqual(
            BODY_MASS.parse(
                '{"created": "2014-10-29", "relatedresourceid": '
                '"57d3efd8-2b9c-4952-8976-e27401a01251;'
                '8a35be5e-27fb-4875-81f6-42a5d7787760"}'),
            [])

    def test_parse_44(self):
        self.assertEqual(
            BODY_MASS.parse('Weight=22 lbs., 7 oz.; Length=41 in. T.L.'),
            [Trait(
                value=10177.48, units=['lbs', 'oz'], units_inferred=False,
                start=0, end=20)])

    def test_parse_45(self):
        self.assertEqual(
            BODY_MASS.parse('{"earLengthInmm":"X", "weightInlbs":"22"}'),
            [Trait(
                value=9979.03, units='lbs', units_inferred=False,
                start=23, end=39)])

    def test_parse_46(self):
        self.assertEqual(
            BODY_MASS.parse('{"measurements":"90-30-16-7=6.9MGS" }'),
            [Trait(
                value=0.01, units='MGS', units_inferred=False,
                is_shorthand=True, start=2, end=34)])

    def test_parse_47(self):
        self.assertEqual(
            BODY_MASS.parse('; unformatted measurements=g 0.24 mm ;'),
            [])
