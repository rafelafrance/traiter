# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods
import unittest
from pylib.vertnet.trait import Trait
from pylib.vertnet.parsers.testes_size import TESTES_SIZE


class TestTestesSize(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            TESTES_SIZE.parse('testes = 8x5 mm'),
            [Trait(
                value=[8, 5], units='mm', units_inferred=False,
                start=0, end=15)])

    def test_parse_02(self):
        self.assertEqual(
            TESTES_SIZE.parse('testes: 20mm. Sent to Berkeley 10/1/71'),
            [Trait(
                value=20, units='mm', units_inferred=False, start=0, end=12)])

    def test_parse_03(self):
        self.assertEqual(
            TESTES_SIZE.parse(
                'ear from notch=19 mm; reproductive data=testis 5mm ; '),
            [Trait(
                value=5, units='mm', units_inferred=False, start=22, end=50)])

    def test_parse_04(self):
        self.assertEqual(
            TESTES_SIZE.parse(
                'adult ; reproductive data=NS; T=9x4 ; endoparasite '),
            [Trait(
                value=[9, 4], units=None, units_inferred=True,
                start=8, end=35)])

    def test_parse_05(self):
        self.assertEqual(
            TESTES_SIZE.parse(
                '2.3 g; reproductive data=testes: 18x8 mm; scrotal ;'),
            [Trait(
                value=[18, 8], units='mm', units_inferred=False,
                start=7, end=40)])

    def test_parse_06(self):
        self.assertEqual(
            TESTES_SIZE.parse('Plus Tissue; plus Baculum: Test 21x11'),
            [Trait(
                value=[21, 11], units=None, units_inferred=True,
                start=27, end=37)])

    def test_parse_07(self):
        self.assertEqual(
            TESTES_SIZE.parse(
                '; reproductive data=testes scrotal; T = 9mm in length'),
            [Trait(
                value=9, units='mm', units_inferred=False, start=2, end=43)])

    def test_parse_08(self):
        self.assertEqual(
            TESTES_SIZE.parse('Scrotal 9 mm x 5 mm'),
            [Trait(
                value=[9, 5], units_inferred=False, units=['mm', 'mm'],
                start=0, end=19)])

    def test_parse_09(self):
        self.assertEqual(
            TESTES_SIZE.parse(
                'reproductive data=testes abdominal; T = 3 x 1.8 ;'),
            [Trait(
                value=[3, 1.8], units=None, units_inferred=True,
                start=0, end=47)])

    def test_parse_10(self):
        self.assertEqual(
            TESTES_SIZE.parse(
                'testis-20mm ; reproductive data=testis-21mm ; '),
            [
                Trait(
                    value=20, units='mm', units_inferred=False,
                    start=0, end=11),
                Trait(
                    value=21, units='mm', units_inferred=False,
                    start=14, end=43)])

    def test_parse_11(self):
        self.assertEqual(
            TESTES_SIZE.parse('Testes x6'),
            [Trait(
                value=6, units=None, units_inferred=True, start=0, end=9)])

    def test_parse_12(self):
        self.assertEqual(
            TESTES_SIZE.parse('testes scrotal, L testis 13x5mm'),
            [Trait(
                value=[13, 5], units='mm', units_inferred=False,
                start=18, end=31)])

    def test_parse_13(self):
        self.assertEqual(
            TESTES_SIZE.parse(
                '"gonad length 1":"3.0", "gonad length 2":"2.0",'),
            [
                Trait(
                    value=3, units=None, units_inferred=True, side='1',
                    dimension='length', ambiguous_key=True, start=1, end=21),
                Trait(
                    value=2, units=None, units_inferred=True, side='2',
                    dimension='length', ambiguous_key=True, start=25, end=45)])

    def test_parse_14(self):
        self.assertEqual(
            TESTES_SIZE.parse('"gonadLengthInMM":"12", "gonadWidthInMM":"5",'),
            [
                Trait(
                    value=12, units='MM', units_inferred=False,
                    ambiguous_key=True, dimension='length', start=1, end=21),
                Trait(
                    value=5, units='MM', units_inferred=False,
                    ambiguous_key=True, dimension='width', start=25, end=43)])

    def test_parse_15(self):
        self.assertEqual(
            TESTES_SIZE.parse(
                'left gonad width=9.1 mm; right gonad width=9.2 mm; '
                'right gonad length=16.1 mm; left gonad length=16.2 mm'),
            [
                Trait(
                    value=9.1, units='mm', units_inferred=False,
                    ambiguous_key=True, side='left',
                    dimension='width', start=0, end=23),
                Trait(
                    value=9.2, units='mm', units_inferred=False,
                    ambiguous_key=True, side='right',
                    dimension='width', start=25, end=49),
                Trait(
                    value=16.1, units='mm', units_inferred=False,
                    ambiguous_key=True, side='right',
                    dimension='length', start=51, end=77),
                Trait(
                    value=16.2, units='mm', units_inferred=False,
                    ambiguous_key=True, side='left',
                    dimension='length', start=79, end=104)])

    def test_parse_16(self):
        self.assertEqual(
            TESTES_SIZE.parse('"gonadLengthInMM":"9mm w.o./epid", '),
            [Trait(
                value=9, units=['MM', 'mm'], units_inferred=False,
                ambiguous_key=True, dimension='length', start=1, end=22)])

    def test_parse_17(self):
        self.assertEqual(
            TESTES_SIZE.parse('testis-7mm'),
            [Trait(
                value=7, units='mm', units_inferred=False, start=0, end=10)])

    def test_parse_18(self):
        self.assertEqual(
            TESTES_SIZE.parse('reproductive data=T=10x4 ; '),
            [Trait(
                value=[10, 4], units=None, units_inferred=True,
                start=0, end=24)])

    def test_parse_19(self):
        self.assertEqual(
            TESTES_SIZE.parse(
                'x=male ; reproductive data=testes abdominal ; '
                'weight=30 g; hind foot with claw=32 mm; ear from '
                'notch=28 mm; tail length=89 mm; unformatted '
                'measurements=196-89-32-28=30 ; total length=196 mm'),
            [])

    def test_parse_20(self):
        self.assertEqual(
            TESTES_SIZE.parse('adult ; T=9x4 ; endoparasite '),
            [Trait(
                value=[9.0, 4.0], units=None, units_inferred=True,
                ambiguous_key=True, start=8, end=13)])

    def test_parse_21(self):
        self.assertEqual(
            TESTES_SIZE.parse('adult ; T=9 ; endoparasite '),
            [Trait(
                value=9, units=None, units_inferred=True, ambiguous_key=True,
                start=8, end=11)])

    def test_parse_22(self):
        self.assertEqual(
            TESTES_SIZE.parse('TESTES 5-3.5 MM,'),
            [Trait(
                value=[5, 3.5], units='MM', units_inferred=False,
                start=0, end=15)])

    def test_parse_23(self):
        self.assertEqual(
            TESTES_SIZE.parse('reproductive data=T: R-2x4mm ; '),
            [Trait(
                value=[2, 4], units='mm', units_inferred=False, side='r',
                start=0, end=28)])

    def test_parse_24(self):
        self.assertEqual(
            TESTES_SIZE.parse('reproductive data=T: L-2x4mm ; '),
            [Trait(
                value=[2, 4], units='mm', units_inferred=False,
                side='l', start=0, end=28)])

    def test_parse_25(self):
        self.assertEqual(
            TESTES_SIZE.parse('testes (R) 6 x 1.5 & 5 x 2 mm'),
            [
                Trait(
                    value=[6.0, 1.5], units='mm', units_inferred=False,
                    side='r', start=0, end=29),
                Trait(
                    value=[5.0, 2.0], units='mm', units_inferred=False,
                    side='l',
                    start=0, end=29)])

    def test_parse_26(self):
        self.assertEqual(
            TESTES_SIZE.parse('Cataloged by: R.L. Humphrey, 31 January 1995'),
            [])

    def test_parse_27(self):
        self.assertEqual(
            TESTES_SIZE.parse('; reproductive data=5x3 inguinal ;'),
            [Trait(
                value=[5, 3], units=None, units_inferred=True,
                start=2, end=23)])

    def test_parse_28(self):
        self.assertEqual(
            TESTES_SIZE.parse(
                "sex=male ; reproductive data=Testes .5' , scrotal"),
            [Trait(
                value=152.4, units="'", units_inferred=False,
                start=11, end=39)])

    def test_parse_29(self):
        self.assertEqual(
            TESTES_SIZE.parse(
                "; reproductive data=TESTES NOT DESCENDED - 6 MM age"),
            [Trait(
                value=6, units="MM", units_inferred=False, start=2, end=47)])

    def test_parse_30(self):
        self.assertEqual(
            TESTES_SIZE.parse(
                'A. Svihla ; verbatim collector=Dept. No. 2025, W. '),
            [])

    def test_parse_31(self):
        self.assertEqual(
            TESTES_SIZE.parse('reproductive data=Right testicle: 20x9 mm ;'),
            [Trait(
                value=[20.0, 9.0], units="mm", units_inferred=False,
                side='right', start=0, end=41)])

    def test_parse_32(self):
        self.assertEqual(
            TESTES_SIZE.parse('; reproductive data=Testes scrotal, 32x11'),
            [Trait(
                value=[32, 11], units=None, units_inferred=True,
                start=2, end=41)])

    def test_parse_33(self):
        self.assertEqual(
            TESTES_SIZE.parse(
                '; reproductive data=R 20mm L x 6 mm Wne scars ;'),
            [Trait(
                value=20, units='mm', units_inferred=False, side='r',
                start=2, end=26)])

    def test_parse_34(self):
        self.assertEqual(
            TESTES_SIZE.parse('; reproductive data=R 20mm L 6 mm ;'),
            [
                Trait(
                    value=20, units='mm', units_inferred=False, side='r',
                    start=2, end=33),
                Trait(
                    value=6, units='mm', units_inferred=False, side='l',
                    start=2, end=33)])

    def test_parse_35(self):
        self.assertEqual(
            TESTES_SIZE.parse('; reproductive data=(R) 20x10mm L 6x4 mm ;'),
            [
                Trait(
                    value=[20, 10], units='mm', units_inferred=False, side='r',
                    start=2, end=40),
                Trait(
                    value=[6, 4], units='mm', units_inferred=False, side='l',
                    start=2, end=40)])

    def test_parse_36(self):
        self.assertEqual(
            TESTES_SIZE.parse('; reproductive data=R 20x10mm ;'),
            [Trait(
                value=[20, 10], units='mm', units_inferred=False, side='r',
                start=2, end=29)])

    def test_parse_37(self):
        self.assertEqual(
            TESTES_SIZE.parse('; reproductive data=t=233mg ;'),
            [])

    def test_parse_38(self):
        self.assertEqual(
            TESTES_SIZE.parse(
                '{"created": "2014-10-29", "relatedresourceid": '
                '"eeba8b10-040e-4477-a0a6-870102b56234;'
                'abbf14f5-1a7c-48f6-8f2f-2a8af53c8c86"}'),
            [])

    def test_parse_39(self):
        self.assertEqual(
            TESTES_SIZE.parse(
                '{"created": "2007-05-27", "relatedresourceid": '
                '"92bc5a20-577e-4504-aab6-bb409d06871a;'
                '0460ccc4-a461-43ec-86b6-1c252377b126"}'),
            [])

    def test_parse_40(self):
        self.assertEqual(
            TESTES_SIZE.parse(
                '{"created": "2014-10-29", "relatedresourceid": '
                '"57d3efd8-2b9c-4952-8976-e27401a01251;'
                '8a35be5e-27fb-4875-81f6-42a5d7787760"}'),
            [])
