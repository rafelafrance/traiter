# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.parsers.reducers import Result
from lib.parsers.parse_total_length import ParseTotalLength


PAR = ParseTotalLength()


class TestParseTotalLength(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('{"totalLengthInMM":"123" };'),
            [Result(value=123.0, has_units=True, start=2, end=23)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('measurements: ToL=230;TaL=115;HF=22;E=18;'
                      ' total length=231 mm; tail length=115 mm;'),
            [Result(value=230.0, has_units=False, start=14, end=21),
             Result(value=231.0, has_units=True, start=42, end=61)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('measurements: ToL=230;TaL=115;HF=22;E=18;'
                      ' total length=24 cm; tail length=115 mm;'),
            [Result(value=230.0, has_units=False, start=14, end=21),
             Result(value=240.0, has_units=True, start=42, end=60)])

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
            [Result(value=308.0, has_units=True, start=3, end=31)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('308-190-45-20'),
            [Result(value=308.0, has_units=True, start=0, end=13)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse((
                'snout-vent length=54 mm; total length=111 mm;'
                ' tail length=57 mm; weight=5 g')),
            [Result(value=111.0, has_units=True, start=25, end=44)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse((
                'unformatted measurements=Verbatim weight=X;'
                'ToL=230;TaL=115;HF=22;E=18;'
                ' total length=231 mm; tail length=115 mm;')),
            [Result(value=230.0, has_units=False, start=43, end=50),
             Result(value=231.0, has_units=True, start=71, end=90)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('143-63-20-17=13'),
            [Result(value=143.0, has_units=True, start=0, end=15)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('** Body length =345 cm; Blubber=1 cm '),
            [Result(value=3450.0, has_units=True, start=3, end=22)])

    def test_parse_12(self):
        self.assertEqual(
            PAR.parse('t.l.= 2 feet 3.1 - 4.5 inches '),
            [Result(value=[688.34, 723.9], has_units=True, start=0, end=29)])

    def test_parse_13(self):
        self.assertEqual(
            PAR.parse('2 ft. 3.1 - 4.5 in. '),
            [Result(value=[688.34, 723.9], has_units=True, start=0, end=19)])

    def test_parse_14(self):
        self.assertEqual(
            PAR.parse('total length= 2 ft.'),
            [Result(value=609.6, has_units=True, start=0, end=19)])

    def test_parse_15(self):
        self.assertEqual(
            PAR.parse('AJR-32   186-102-23-15  15.0g'),
            [Result(value=186.0, has_units=True, start=9, end=28)])

    def test_parse_16(self):
        self.assertEqual(
            PAR.parse('length=8 mm'),
            [Result(
                value=8.0, has_units=True, ambiguous=True, start=0, end=11)])

    def test_parse_17(self):
        self.assertEqual(
            PAR.parse('another; length=8 mm'),
            [Result(
                value=8.0, has_units=True, ambiguous=True, start=9, end=20)])

    def test_parse_18(self):
        self.assertEqual(
            PAR.parse('another; TL_120, noise'),
            [Result(
                value=120.0, has_units=False, start=9, end=15)])

    def test_parse_19(self):
        self.assertEqual(
            PAR.parse('another; TL - 101.3mm, noise'),
            [Result(
                value=101.3, has_units=True, start=9, end=21)])

    def test_parse_20(self):
        self.assertEqual(
            PAR.parse('before; TL153, after'),
            [Result(
                value=153.0, has_units=False, start=8, end=13)])

    def test_parse_21(self):
        self.assertEqual(
            PAR.parse((
                'before; Total length in catalog and '
                'specimen tag as 117, after')),
            [])

    def test_parse_22(self):
        self.assertEqual(
            #    0123456789.123456789.123456789.123456789.123456789.12345
            PAR.parse('before Snout vent lengths range from 16 to 23 mm. qq'),
            [Result(
                value=[16.0, 23.0],
                has_units=True,
                start=7, end=49)])
