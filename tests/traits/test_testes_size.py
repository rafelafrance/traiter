# flake8=noqa

import unittest
from lib.parse_result import ParseResult
from lib.traits.testes_size import TestesSize


PAR = TestesSize()


class TestTestesSize(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('testes = 8x5 mm'),
            [ParseResult(value=[8, 5], units='mm', start=0, end=15)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('testes: 20mm. Sent to Berkeley 10/1/71'),
            [ParseResult(value=20, units='mm', start=0, end=12)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('ear from notch=19 mm; reproductive data=testis 5mm ; '),
            [ParseResult(value=5, units='mm', start=22, end=50)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('adult ; reproductive data=NS; T=9x4 ; endoparasite '),
            [ParseResult(
                value=[9, 4],
                flags={'units_inferred': True},
                start=8, end=35)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('2.3 g; reproductive data=testes: 18x8 mm; scrotal ;'),
            [ParseResult(value=[18, 8], units='mm', start=7, end=40)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('Plus Tissue; plus Baculum: Test 21x11'),
            [ParseResult(
                value=[21, 11],
                flags={'units_inferred': True},
                start=27, end=37)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('; reproductive data=testes scrotal; T = 9mm in length'),
            [ParseResult(value=9, units='mm', start=2, end=43)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('Scrotal 9 mm x 5 mm'),
            [ParseResult(value=[9, 5], units='mm', start=0, end=19)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('reproductive data=testes abdominal; T = 3 x 1.8 ;'),
            [ParseResult(
                value=[3, 1.8],
                flags={'units_inferred': True},
                start=0, end=47)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('testis-20mm ; reproductive data=testis-21mm ; '),
            [ParseResult(value=20, units='mm', start=0, end=11),
             ParseResult(value=21, units='mm', start=14, end=43)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('Testes x6'),
            [ParseResult(
                value=6,
                flags={'units_inferred': True},
                start=0, end=9)])

    def test_parse_12(self):
        self.assertEqual(
            PAR.parse('testes scrotal, L testis 13x5mm'),
            [ParseResult(value=[13, 5], units='mm', start=0, end=31)])

    def test_parse_13(self):
        self.maxDiff = None
        self.assertEqual(
            PAR.parse('"gonad length 1":"3.0", "gonad length 2":"2.0",'),
            [ParseResult(
                value=3,
                flags={'units_inferred': True,
                       'index': '1',
                       'ambiguous_sex': True},
                start=1, end=21),
             ParseResult(
                value=2,
                flags={'units_inferred': True,
                       'index': '2',
                       'ambiguous_sex': True},
                start=25, end=45)])

    def test_parse_14(self):
        self.maxDiff = None
        self.assertEqual(
            PAR.parse('"gonadLengthInMM":"12", "gonadWidthInMM":"5",'),
            [ParseResult(
                value=12, units='gonadlengthinmm',
                flags={'ambiguous_sex': True},
                start=1, end=21),
             ParseResult(
                value=5, units='gonadwidthinmm',
                flags={'ambiguous_sex': True},
                start=25, end=43)])

    def test_parse_15(self):
        self.maxDiff = None
        self.assertEqual(
            PAR.parse('left gonad width=9.1 mm; right gonad width=9.2 mm; '
                      'right gonad length=16.1 mm; left gonad length=16.2 mm'),
            [ParseResult(
                value=9.1, units='mm',
                flags={'ambiguous_sex': True, 'side': 'left'},
                start=0, end=23),
             ParseResult(
                value=9.2, units='mm',
                flags={'ambiguous_sex': True, 'side': 'right'},
                start=25, end=49),
             ParseResult(
                value=16.1, units='mm',
                flags={'ambiguous_sex': True, 'side': 'right'},
                start=51, end=77),
             ParseResult(
                value=16.2, units='mm',
                flags={'ambiguous_sex': True, 'side': 'left'},
                start=79, end=104)])

    def test_parse_16(self):
        self.assertEqual(
            PAR.parse('"gonadLengthInMM":"9mm w.o./epid", '),
            [ParseResult(
                value=9, units='gonadlengthinmm',
                flags={'ambiguous_sex': True},
                start=1, end=22)])

    def test_parse_17(self):
        self.assertEqual(
            PAR.parse('testis-7mm'),
            [ParseResult(value=7, units='mm', start=0, end=10)])

    def test_parse_18(self):
        self.assertEqual(
            PAR.parse('reproductive data=T=10x4 ; '),
            [ParseResult(
                value=[10, 4],
                flags={'units_inferred': True},
                start=0, end=24)])