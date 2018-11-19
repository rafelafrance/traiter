# pylint: disable=missing-docstring,import-error,too-many-public-methods

from argparse import Namespace
import unittest
from lib.trait_parsers.total_length import ParseTotalLength


class TestTotalLengthParser(unittest.TestCase):

    def test_parser_01(self):
        self.assertDictEqual(
            TARGET.parse(['{"totalLengthInMM":"123" };']),
            {'key': 'totalLengthInMM',
             'value': '123',
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 2,
             'end': 23,
             'units': 'MM'})

    def test_parser_02(self):
        self.assertDictEqual(
            TARGET.parse([
                'measurements: ToL=230;TaL=115;HF=22;E=18;'
                ' total length=230 mm; tail length=115 mm;']),
            {'key': 'total length',
             'value': '230',
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 42,
             'end': 61,
             'units': 'mm'})

    def test_parser_03(self):
        self.assertEqual(
            TARGET.parse(['sex=unknown ; crown-rump length=8 mm']),
            None)

    def test_parser_04(self):
        self.assertEqual(
            TARGET.parse([
                'left gonad length=10 mm; right gonad length=10 mm;']),
            None)

    def test_parser_05(self):
        self.assertDictEqual(
            TARGET.parse(['"{"measurements":"308-190-45-20" }"']),
            {'key': 'measurements',
             'value': '308',
             'regex': 'len_shorthand',
             'field': 'col1',
             'start': 3,
             'end': 31,
             'units': '_mm_'})

    def test_parser_06(self):
        self.assertDictEqual(
            TARGET.parse(['308-190-45-20']),
            {'key': '_shorthand_',
             'value': '308',
             'regex': 'len_shorthand',
             'field': 'col1',
             'start': 0,
             'end': 13,
             'units': '_mm_'})

    def test_parser_07(self):
        self.assertDictEqual(
            TARGET.parse(['{"measurements":"143-63-20-17=13 g" }']),
            {'key': 'measurements',
             'value': '143',
             'regex': 'len_shorthand',
             'field': 'col1',
             'start': 2,
             'end': 29,
             'units': '_mm_'})

    def test_parser_08(self):
        self.assertDictEqual(
            TARGET.parse(['143-63-20-17=13']),
            {'key': '_shorthand_',
             'value': '143',
             'regex': 'len_shorthand',
             'field': 'col1',
             'start': 0,
             'end': 12,
             'units': '_mm_'})

    def test_parser_09(self):
        self.assertDictEqual(
            TARGET.parse([
                'snout-vent length=54 mm; total length=111 mm;'
                ' tail length=57 mm; weight=5 g']),
            {'key': 'total length',
             'value': '111',
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 25,
             'end': 44,
             'units': 'mm'})

    def test_parser_10(self):
        self.assertDictEqual(
            TARGET.parse([
                'unformatted measurements=Verbatim weight=X;'
                'ToL=230;TaL=115;HF=22;E=18;'
                ' total length=230 mm; tail length=115 mm;']),
            {'key': 'total length',
             'value': '230',
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 71,
             'end': 90,
             'units': 'mm'})

    def test_parser_11(self):
        self.assertDictEqual(
            TARGET.parse(['** Body length =345 cm; Blubber=1 cm ']),
            {'key': 'Body length',
             'value': '345',
             'regex': 'other_len_key',
             'field': 'col1',
             'start': 3,
             'end': 22,
             'units': 'cm'})

    def test_parser_12(self):
        self.assertDictEqual(
            TARGET.parse(['t.l.= 2 feet 3.1 - 4.5 inches ']),
            {'key': 't.l.',
             'value': ['2', '3.1 - 4.5'],
             'regex': 'en_len',
             'field': 'col1',
             'start': 0,
             'end': 29,
             'units': ['feet', 'inches']})

    def test_parser_13(self):
        self.assertDictEqual(
            TARGET.parse(['2 ft. 3.1 - 4.5 in. ']),
            {'key': '_english_',
             'value': ['2', '3.1 - 4.5'],
             'regex': 'en_len',
             'field': 'col1',
             'start': 0,
             'end': 19,
             'units': ['ft.', 'in.']})

    def test_parser_14(self):
        self.assertDictEqual(
            TARGET.parse(['total length= 2 ft.']),
            {'key': 'total length',
             'value': '2',
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 0,
             'end': 19,
             'units': 'ft.'})

    def test_parser_15(self):
        self.assertDictEqual(
            TARGET.parse(['AJR-32   186-102-23-15  15.0g']),
            {'key': '_shorthand_',
             'value': '186',
             'regex': 'len_shorthand',
             'field': 'col1',
             'start': 9,
             'end': 22,
             'units': '_mm_'})

    def test_parser_16(self):
        self.assertDictEqual(
            TARGET.parse(['length=8 mm']),
            {'key': 'length',
             'value': '8',
             'regex': 'len_key_ambiguous_units',
             'field': 'col1',
             'start': 0,
             'end': 11,
             'units': 'mm'})

    def test_parser_17(self):
        self.assertDictEqual(
            TARGET.parse(['another; length=8 mm']),
            {'key': 'length',
             'value': '8',
             'regex': 'len_key_ambiguous_units',
             'field': 'col1',
             'start': 7,
             'end': 20,
             'units': 'mm'})

    def test_parser_18(self):
        self.assertDictEqual(
            TARGET.parse(['another; TL_120, noise']),
            {'key': 'TL_',
             'value': '120',
             'regex': 'other_len_key',
             'field': 'col1',
             'start': 9,
             'end': 15,
             'units': None})

    def test_parser_19(self):
        self.assertDictEqual(
            TARGET.parse(['another; TL - 101.3mm, noise']),
            {'key': 'TL',
             'value': '101.3',
             'regex': 'other_len_key',
             'field': 'col1',
             'start': 9,
             'end': 21,
             'units': 'mm'})

    def test_parser_20(self):
        self.assertDictEqual(
            TARGET.parse(['before; TL153, after']),
            {'key': 'TL',
             'value': '153',
             'regex': 'other_len_key',
             'field': 'col1',
             'start': 8,
             'end': 13,
             'units': None})

    def test_parser_21(self):
        self.assertDictEqual(
            TARGET.parse([
                'before; Total length in catalog and '
                'specimen tag as 117, after']),
            {'key': 'Total length',
             'value': '117',
             'regex': 'len_in_phrase',
             'field': 'col1',
             'start': 8,
             'end': 55,
             'units': None})

    def test_parser_22(self):
        self.assertDictEqual(
            TARGET.parse([
                'before Snout vent lengths range from 16 to 23 mm. after']),
            {'key': 'Snout vent lengths',
             'value': '16 to 23',
             'regex': 'len_in_phrase',
             'field': 'col1',
             'start': 7,
             'end': 49,
             'units': 'mm.'})

    def test_parser_23(self):
        self.assertDictEqual(
            TARGET.parse(['Size=13 cm TL']),
            {'key': 'TL',
             'value': '13',
             'regex': 'len_key_suffix',
             'field': 'col1',
             'start': 5,
             'end': 13,
             'units': 'cm'})

    def test_parser_24(self):
        self.assertDictEqual(
            TARGET.parse(['det_comments:31.5-58.3inTL']),
            {'key': 'TL',
             'value': '31.5-58.3',
             'regex': 'len_key_suffix',
             'field': 'col1',
             'start': 13,
             'end': 26,
             'units': 'in'})

    def test_parser_25(self):
        self.assertDictEqual(
            TARGET.parse(['SVL52mm']),
            {'key': 'SVL',
             'value': '52',
             'regex': 'svl_len_key',
             'field': 'col1',
             'start': 0,
             'end': 7,
             'units': 'mm'})

    def test_parser_26(self):
        self.assertDictEqual(
            TARGET.parse([
                'snout-vent length=221 mm; total length=257 mm; '
                'tail length=36 mm']),
            {'key': 'total length',
             'value': '257',
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 26,
             'end': 45,
             'units': 'mm'})

    def test_parser_27(self):
        self.assertDictEqual(
            TARGET.parse(['SVL 209 mm, total 272 mm, 4.4 g.']),
            {'key': 'total',
             'value': '272',
             'regex': 'key_units_req',
             'field': 'col1',
             'start': 12,
             'end': 24,
             'units': 'mm'})

    def test_parser_28(self):
        self.assertDictEqual(
            TARGET.parse(['{"time collected":"0712-0900", "length":"12.0" }']),
            {'key': 'length',
             'value': '12.0',
             'regex': 'len_key_ambiguous',
             'field': 'col1',
             'start': 31,
             'end': 45,
             'units': None})

    def test_parser_29(self):
        self.assertDictEqual(
            TARGET.parse([
                '{"time collected":"1030", "water depth":"1-8", '
                '"bottom":"abrupt lava '
                'cliff dropping off to sand at 45 ft.", '
                '"length":"119-137" }']),
            {'key': 'length',
             'value': '119-137',
             'regex': 'len_key_ambiguous',
             'field': 'col1',
             'start': 108,
             'end': 125,
             'units': None})

    def test_parser_30(self):
        self.assertDictEqual(
            TARGET.parse(['TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx']),
            {'key': 'TL',
             'value': '44',
             'regex': 'len_key_abbrev',
             'field': 'col1',
             'start': 0,
             'end': 10,
             'units': 'mm'})

    def test_parser_31(self):
        self.assertDictEqual(
            TARGET.parse(['{"totalLengthInMM":"270-165-18-22-31", ']),
            {'key': 'totalLengthInMM',
             'value': '270',
             'regex': 'len_shorthand',
             'field': 'col1',
             'start': 2,
             'end': 36,
             'units': 'MM'})

    def test_parser_32(self):
        self.assertDictEqual(
            TARGET.parse(['{"length":"20-29" }']),
            {'key': 'length',
             'value': '20-29',
             'regex': 'len_key_ambiguous',
             'field': 'col1',
             'start': 0,
             'end': 16,
             'units': None})

    def test_parser_33(self):
        self.assertDictEqual(
            TARGET.parse([
                'field measurements on fresh dead specimen '
                'were 157-60-20-19-21g']),
            {'key': '_shorthand_',
             'value': '157',
             'regex': 'len_shorthand',
             'field': 'col1',
             'start': 47,
             'end': 62,
             'units': '_mm_'})

    def test_parser_34(self):
        self.assertDictEqual(
            TARGET.parse(['f age class: adult; standard length: 63-107mm']),
            {'key': 'standard length',
             'value': '63-107',
             'regex': 'total_len_key',
             'field': 'col1',
             'start': 20,
             'end': 45,
             'units': 'mm'})

    def test_parser_35(self):
        self.assertEqual(
            TARGET.parse(['Rehydrated in acetic acid 7/1978-8/1987.']),
            None)

    def test_parser_36(self):
        self.assertDictEqual(
            TARGET.parse(['age class: adult; standard length: 18.0-21.5mm']),
            {'key': 'standard length',
             'value': '18.0-21.5',
             'regex': 'total_len_key',
             'field': 'col1',
             'start': 18,
             'end': 46,
             'units': 'mm'})

    def test_parser_37(self):
        self.assertDictEqual(
            TARGET.parse(['age class: adult; standard length: 18-21.5mm']),
            {'key': 'standard length',
             'value': '18-21.5',
             'regex': 'total_len_key',
             'field': 'col1',
             'start': 18,
             'end': 44,
             'units': 'mm'})

    def test_parser_38(self):
        self.assertDictEqual(
            TARGET.parse(['age class: adult; standard length: 18.0-21mm']),
            {'key': 'standard length',
             'value': '18.0-21',
             'regex': 'total_len_key',
             'field': 'col1',
             'start': 18,
             'end': 44,
             'units': 'mm'})

    def test_parser_39(self):
        self.assertDictEqual(
            TARGET.parse(['age class: adult; standard length: 18-21mm']),
            {'key': 'standard length',
             'value': '18-21',
             'regex': 'total_len_key',
             'field': 'col1',
             'start': 18,
             'end': 42,
             'units': 'mm'})

    def test_parser_40(self):
        self.assertEqual(
            TARGET.parse([
                "Specimen #'s - 5491,5492,5498,5499,5505,5526,5527,5528,5500,"
                "5507,5508,5590,5592,95,5594,5593,5596,5589,5587,5586,5585"]),
            None)

    def test_parser_41(self):
        self.assertEqual(
            TARGET.parse(['20-28mm SL']),
            {'key': 'SL',
             'value': '20-28',
             'regex': 'len_key_suffix',
             'field': 'col1',
             'start': 0,
             'end': 10,
             'units': 'mm'})

    def test_parser_42(self):
        self.assertEqual(
            TARGET.parse(['29mm SL']),
            {'key': 'SL',
             'value': '29',
             'regex': 'len_key_suffix',
             'field': 'col1',
             'start': 0,
             'end': 7,
             'units': 'mm'})

    def test_parser_43(self):
        self.assertEqual(
            TARGET.parse(['{"measurements":"159-?-22-16=21.0" }']),
            {'key': 'measurements',
             'value': '159',
             'regex': 'len_shorthand',
             'field': 'col1',
             'start': 2,
             'end': 28,
             'units': '_mm_'})

    def test_parser_44(self):
        self.assertEqual(
            TARGET.parse(['c701563b-dbd9-4500-184f-1ad61eb8da11']),
            None)

    def test_parser_45(self):
        self.assertEqual(
            TARGET.parse(['Meas: L: 21.0']),
            {'key': 'Meas: L',
             'value': '21.0',
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 0,
             'end': 13,
             'units': '_mm_'})

    def test_parser_46(self):
        self.assertEqual(
            TARGET.parse(['Meas: L: 21.0 cm']),
            {'key': 'Meas: L',
             'value': '21.0',
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 0,
             'end': 16,
             'units': 'cm'})

    def test_parser_47(self):
        self.assertEqual(
            TARGET.parse(['LABEL. LENGTH 375 MM.']),
            {'key': 'LABEL. LENGTH',
             'value': '375',
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 0,
             'end': 21,
             'units': 'MM.'})

    def test_parser_48(self):
        self.assertEqual(
            TARGET.parse(['SL=12mm']),
            {'key': 'SL',
             'value': '12',
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 0,
             'end': 7,
             'units': 'mm'})

    def test_parser_49(self):
        self.assertEqual(
            TARGET.parse(['Size=SL 12-14 mm']),
            {'key': 'SL',
             'value': '12-14',
             'regex': 'total_len_key',
             'field': 'col1',
             'start': 5,
             'end': 16,
             'units': 'mm'})

    def test_parser_50(self):
        self.assertEqual(
            TARGET.parse(['SV 1.2']),
            {'key': 'SV',
             'value': '1.2',
             'regex': 'svl_len_key',
             'field': 'col1',
             'start': 0,
             'end': 6,
             'units': None})

    def test_parser_51(self):
        self.assertEqual(
            TARGET.parse([' Length: 123 mm SL']),
            {'key': 'SL',
             'value': '123',
             'regex': 'len_key_suffix',
             'field': 'col1',
             'start': 9,
             'end': 18,
             'units': 'mm'})

    def test_parser_52(self):
        self.assertEqual(
            TARGET.parse([' Length: 12-34 mmSL']),
            {'key': 'SL',
             'value': '12-34',
             'regex': 'len_key_suffix',
             'field': 'col1',
             'start': 9,
             'end': 19,
             'units': 'mm'})

    def test_parser_53(self):
        self.assertEqual(
            TARGET.parse(['Measurements: L: 21.0 cm']),
            {'key': 'Measurements: L',
             'value': '21.0',
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 0,
             'end': 24,
             'units': 'cm'})

    def test_parser_54(self):
        self.assertEqual(
            TARGET.parse(['SVL=44']),
            {'key': 'SVL',
             'value': '44',
             'regex': 'svl_len_key',
             'field': 'col1',
             'start': 0,
             'end': 6,
             'units': None})

    def test_parser_55(self):
        self.assertDictEqual(
            TARGET.parse(['Total Length: 185 - 252 mm']),
            {'key': 'Total Length',
             'regex': 'total_len_key',
             'value': '185 - 252',
             'field': 'col1',
             'start': 0,
             'end': 26,
             'units': 'mm'})

    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################

    def test_search_and_normalize_01(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['{"totalLengthInMM":"123" };']),
            {'found': True,
             'millimeters': 123,
             'units_inferred': False,
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 2,
             'end': 23,
             'key': 'totalLengthInMM'})

    def test_search_and_normalize_02(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['measurements: ToL=230;TaL=115;HF=22;E=18; total '
                 'length=230 mm; tail length=115 mm;']),
            {'found': True,
             'millimeters': 230,
             'units_inferred': False,
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 42,
             'end': 61,
             'key': 'total length'})

    def test_search_and_normalize_03(self):
        self.assertEqual(
            TARGET.search_and_normalize(
                ['sex=unknown ; crown-rump length=8 mm']),
            {'found': False,
             'millimeters': None,
             'units_inferred': False,
             'regex': None,
             'field': None,
             'start': None,
             'end': None,
             'key': None})

    def test_search_and_normalize_04(self):
        self.assertEqual(
            TARGET.search_and_normalize(
                ['left gonad length=10 mm; right gonad length=10 mm;']),
            {'found': False,
             'millimeters': None,
             'units_inferred': False,
             'regex': None,
             'field': None,
             'start': None,
             'end': None,
             'key': None})

    def test_search_and_normalize_05(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['"{"measurements":"308-190-45-20" }"']),
            {'found': True,
             'millimeters': 308,
             'units_inferred': True,
             'regex': 'len_shorthand',
             'field': 'col1',
             'start': 3,
             'end': 31,
             'key': 'measurements'})

    def test_search_and_normalize_06(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['308-190-45-20']),
            {'found': True,
             'millimeters': 308,
             'units_inferred': True,
             'regex': 'len_shorthand',
             'field': 'col1',
             'start': 0,
             'end': 13,
             'key': '_shorthand_'})

    def test_search_and_normalize_07(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['{"measurements":"143-63-20-17=13 g" }']),
            {'found': True,
             'millimeters': 143,
             'units_inferred': True,
             'regex': 'len_shorthand',
             'field': 'col1',
             'start': 2,
             'end': 29,
             'key': 'measurements'})

    def test_search_and_normalize_08(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['143-63-20-17=13']),
            {'found': True,
             'millimeters': 143,
             'units_inferred': True,
             'regex': 'len_shorthand',
             'field': 'col1',
             'start': 0,
             'end': 12,
             'key': '_shorthand_'})

    def test_search_and_normalize_09(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['snout-vent length=54 mm; total length=111 mm; '
                 'tail length=57 mm; weight=5 g']),
            {'found': True,
             'millimeters': 111,
             'units_inferred': False,
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 25,
             'end': 44,
             'key': 'total length'})

    def test_search_and_normalize_10(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['unformatted measurements=Verbatim weight=X;ToL=230;TaL=115;'
                 'HF=22;E=18; total length=230 mm; tail length=115 mm;']),
            {'found': True,
             'millimeters': 230,
             'units_inferred': False,
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 71,
             'end': 90,
             'key': 'total length'})

    def test_search_and_normalize_11(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['** Body length =345 cm; Blubber=1 cm ']),
            {'found': True,
             'millimeters': 3450,
             'units_inferred': False,
             'regex': 'other_len_key',
             'field': 'col1',
             'start': 3,
             'end': 22,
             'key': 'Body length'})

    def test_search_and_normalize_12(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['t.l.= 2 feet 3.1 - 4.5 inches ']),
            {'found': True,
             'millimeters': [688.7, 724.3],
             'units_inferred': False,
             'regex': 'en_len',
             'field': 'col1',
             'start': 0,
             'end': 29,
             'key': 't.l.'})

    def test_search_and_normalize_13(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['2 ft. 3.1 - 4.5 in. ']),
            {'found': True,
             'millimeters': [688.7, 724.3],
             'units_inferred': False,
             'regex': 'en_len',
             'field': 'col1',
             'start': 0,
             'end': 19,
             'key': '_english_'})

    def test_search_and_normalize_14(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['total length= 2 ft.']),
            {'found': True,
             'millimeters': 610,
             'units_inferred': False,
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 0,
             'end': 19,
             'key': 'total length'})

    def test_search_and_normalize_15(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['AJR-32   186-102-23-15  15.0g']),
            {'found': True,
             'millimeters': 186,
             'units_inferred': True,
             'regex': 'len_shorthand',
             'field': 'col1',
             'start': 9,
             'end': 22,
             'key': '_shorthand_'})

    def test_search_and_normalize_16(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['length=8 mm']),
            {'found': True,
             'millimeters': 8,
             'units_inferred': False,
             'regex': 'len_key_ambiguous_units',
             'field': 'col1',
             'start': 0,
             'end': 11,
             'key': 'length'})

    def test_search_and_normalize_17(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['another; length=8 mm']),
            {'found': True,
             'millimeters': 8,
             'units_inferred': False,
             'regex': 'len_key_ambiguous_units',
             'field': 'col1',
             'start': 7,
             'end': 20,
             'key': 'length'})

    def test_search_and_normalize_18(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['another; TL_120, noise']),
            {'found': True,
             'millimeters': 120,
             'units_inferred': True,
             'regex': 'other_len_key',
             'field': 'col1',
             'start': 9,
             'end': 15,
             'key': 'TL_'})

    def test_search_and_normalize_19(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['another; TL - 101.3mm, noise']),
            {'found': True,
             'millimeters': 101.3,
             'units_inferred': False,
             'regex': 'other_len_key',
             'field': 'col1',
             'start': 9,
             'end': 21,
             'key': 'TL'})

    def test_search_and_normalize_20(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['before; TL153, after']),
            {'found': True,
             'millimeters': 153,
             'units_inferred': True,
             'regex': 'other_len_key',
             'field': 'col1',
             'start': 8,
             'end': 13,
             'key': 'TL'})

    def test_search_and_normalize_21(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['before; Total length in catalog and specimen tag as '
                 '117, after']),
            {'found': True,
             'millimeters': 117,
             'units_inferred': True,
             'regex': 'len_in_phrase',
             'field': 'col1',
             'start': 8,
             'end': 55,
             'key': 'Total length'})

    def test_search_and_normalize_22(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['before Snout vent lengths range from 16 to 23 mm. after']),
            {'found': True,
             'millimeters': [16, 23],
             'units_inferred': False,
             'regex': 'len_in_phrase',
             'field': 'col1',
             'start': 7,
             'end': 49,
             'key': 'Snout vent lengths'})

    def test_search_and_normalize_23(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['Size=13 cm TL']),
            {'found': True,
             'millimeters': 130,
             'units_inferred': False,
             'regex': 'len_key_suffix',
             'field': 'col1',
             'start': 5,
             'end': 13,
             'key': 'TL'})

    def test_search_and_normalize_24(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['det_comments:31.5-58.3inTL']),
            {'found': True,
             'millimeters': [800.1, 1480.8],
             'units_inferred': False,
             'regex': 'len_key_suffix',
             'field': 'col1',
             'start': 13,
             'end': 26,
             'key': 'TL'})

    def test_search_and_normalize_25(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['SVL52mm']),
            {'found': True,
             'millimeters': 52,
             'units_inferred': False,
             'regex': 'svl_len_key',
             'field': 'col1',
             'start': 0,
             'end': 7,
             'key': 'SVL'})

    def test_search_and_normalize_26(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['snout-vent length=221 mm; total length=257 mm; '
                 'tail length=36 mm']),
            {'found': True,
             'millimeters': 257,
             'units_inferred': False,
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 26,
             'end': 45,
             'key': 'total length'})

    def test_search_and_normalize_27(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['SVL 209 mm, total 272 mm, 4.4 g.']),
            {'found': True,
             'millimeters': 272,
             'units_inferred': False,
             'regex': 'key_units_req',
             'field': 'col1',
             'start': 12,
             'end': 24,
             'key': 'total'})

    def test_search_and_normalize_28(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['{"time collected":"0712-0900", "length":"12.0" }']),
            {'found': True,
             'millimeters': 12.0,
             'units_inferred': True,
             'regex': 'len_key_ambiguous',
             'field': 'col1',
             'start': 31,
             'end': 45,
             'key': 'length'})

    def test_search_and_normalize_29(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['{"time collected":"1030", "water depth":"1-8", '
                 '"bottom":"abrupt lava cliff dropping off to sand at '
                 '45 ft.", "length":"119-137" }']),
            {'found': True,
             'millimeters': [119, 137],
             'units_inferred': True,
             'regex': 'len_key_ambiguous',
             'field': 'col1',
             'start': 108,
             'end': 125,
             'key': 'length'})

    def test_search_and_normalize_30(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx']),
            {'found': True,
             'millimeters': 44,
             'units_inferred': False,
             'regex': 'len_key_abbrev',
             'field': 'col1',
             'start': 0,
             'end': 10,
             'key': 'TL'})

    def test_search_and_normalize_31(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['{"totalLengthInMM":"270-165-18-22-31", ']),
            {'found': True,
             'millimeters': 270,
             'units_inferred': False,
             'regex': 'len_shorthand',
             'field': 'col1',
             'start': 2,
             'end': 36,
             'key': 'totalLengthInMM'})

    def test_search_and_normalize_32(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['{"length":"20-29" }']),
            {'found': True,
             'millimeters': [20, 29],
             'units_inferred': True,
             'regex': 'len_key_ambiguous',
             'field': 'col1',
             'start': 0,
             'end': 16,
             'key': 'length'})

    def test_search_and_normalize_33(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['field measurements on fresh dead specimen were '
                 '157-60-20-19-21g']),
            {'found': True,
             'millimeters': 157,
             'units_inferred': True,
             'regex': 'len_shorthand',
             'field': 'col1',
             'start': 47,
             'end': 62,
             'key': '_shorthand_'})

    def test_search_and_normalize_34(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['f age class: adult; standard length: 63-107mm']),
            {'found': True,
             'millimeters': [63, 107],
             'units_inferred': False,
             'regex': 'total_len_key',
             'field': 'col1',
             'start': 20,
             'end': 45,
             'key': 'standard length'})

    def test_search_and_normalize_35(self):
        self.assertEqual(
            TARGET.search_and_normalize(
                ['Rehydrated in acetic acid 7/1978-8/1987.']),
            {'found': False,
             'millimeters': None,
             'units_inferred': False,
             'field': None,
             'start': None,
             'end': None,
             'regex': None,
             'key': None})

    def test_search_and_normalize_36(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['age class: adult; standard length: 18.0-21.5mm']),
            {'found': True,
             'millimeters': [18.0, 21.5],
             'units_inferred': False,
             'regex': 'total_len_key',
             'field': 'col1',
             'start': 18,
             'end': 46,
             'key': 'standard length'})

    def test_search_and_normalize_37(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['age class: adult; standard length: 18-21.5mm']),
            {'found': True,
             'millimeters': [18, 21.5],
             'units_inferred': False,
             'regex': 'total_len_key',
             'field': 'col1',
             'start': 18,
             'end': 44,
             'key': 'standard length'})

    def test_search_and_normalize_38(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['age class: adult; standard length: 18.0-21mm']),
            {'found': True,
             'millimeters': [18.0, 21],
             'units_inferred': False,
             'regex': 'total_len_key',
             'field': 'col1',
             'start': 18,
             'end': 44,
             'key': 'standard length'})

    def test_search_and_normalize_39(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['age class: adult; standard length: 18-21mm']),
            {'found': True,
             'millimeters': [18, 21],
             'units_inferred': False,
             'regex': 'total_len_key',
             'field': 'col1',
             'start': 18,
             'end': 42,
             'key': 'standard length'})

    def test_search_and_normalize_40(self):
        self.assertEqual(
            TARGET.search_and_normalize(
                "Specimen #'s - 5491,5492,5498,5499,5505,5526,5527,5528,5500,"
                "5507,5508,5590,5592,5595,5594,5593,5596,5589,5587,5586,5585"),
            {'found': False,
             'millimeters': None,
             'units_inferred': False,
             'regex': None,
             'field': None,
             'start': None,
             'end': None,
             'key': None})

    def test_search_and_normalize_41(self):
        self.assertEqual(
            TARGET.search_and_normalize(['20-28mm SL']),
            {'found': True,
             'millimeters': [20, 28],
             'units_inferred': False,
             'regex': 'len_key_suffix',
             'field': 'col1',
             'start': 0,
             'end': 10,
             'key': 'SL'})

    def test_search_and_normalize_42(self):
        self.assertEqual(
            TARGET.search_and_normalize(['29mm SL']),
            {'found': True,
             'millimeters': 29,
             'units_inferred': False,
             'regex': 'len_key_suffix',
             'field': 'col1',
             'start': 0,
             'end': 7,
             'key': 'SL'})

    def test_search_and_normalize_43(self):
        self.assertEqual(
            TARGET.search_and_normalize(
                ['{"measurements":"159-?-22-16=21.0" }']),
            {'found': True,
             'millimeters': 159,
             'units_inferred': True,
             'regex': 'len_shorthand',
             'field': 'col1',
             'start': 2,
             'end': 28,
             'key': 'measurements'})

    def test_search_and_normalize_44(self):
        self.assertEqual(
            TARGET.search_and_normalize(
                ['c701563b-dbd9-4500-184f-1ad61eb8da11']),
            {'found': False,
             'millimeters': None,
             'units_inferred': False,
             'regex': None,
             'field': None,
             'start': None,
             'end': None,
             'key': None})

    def test_search_and_normalize_45(self):
        self.assertEqual(
            TARGET.search_and_normalize(['Meas: L: 21.0']),
            {'found': True,
             'millimeters': 21.0,
             'units_inferred': True,
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 0,
             'end': 13,
             'key': 'Meas: L'})

    def test_search_and_normalize_46(self):
        self.assertEqual(
            TARGET.search_and_normalize(['Meas: L: 21.0 cm']),
            {'found': True,
             'millimeters': 210.0,
             'units_inferred': False,
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 0,
             'end': 16,
             'key': 'Meas: L'})

    def test_search_and_normalize_47(self):
        self.assertEqual(
            TARGET.search_and_normalize(['LABEL. LENGTH 375 MM.']),
            {'found': True,
             'millimeters': 375,
             'units_inferred': False,
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 0,
             'end': 21,
             'key': 'LABEL. LENGTH'})

    def test_search_and_normalize_48(self):
        self.assertEqual(
            TARGET.search_and_normalize(['SL=12mm']),
            {'found': True,
             'millimeters': 12,
             'units_inferred': False,
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 0,
             'end': 7,
             'key': 'SL'})

    def test_search_and_normalize_49(self):
        self.assertEqual(
            TARGET.search_and_normalize(['Size=SL 12-14 mm']),
            {'found': True,
             'millimeters': [12, 14],
             'units_inferred': False,
             'regex': 'total_len_key',
             'field': 'col1',
             'start': 5,
             'end': 16,
             'key': 'SL'})

    def test_search_and_normalize_50(self):
        self.assertEqual(
            TARGET.search_and_normalize(['SV 1.2']),
            {'found': True,
             'millimeters': 1.2,
             'units_inferred': True,
             'regex': 'svl_len_key',
             'field': 'col1',
             'start': 0,
             'end': 6,
             'key': 'SV'})

    def test_search_and_normalize_51(self):
        self.assertEqual(
            TARGET.search_and_normalize([' Length: 123 mm SL']),
            {'found': True,
             'millimeters': 123,
             'units_inferred': False,
             'regex': 'len_key_suffix',
             'field': 'col1',
             'start': 9,
             'end': 18,
             'key': 'SL'})

    def test_search_and_normalize_52(self):
        self.assertEqual(
            TARGET.search_and_normalize([' Length: 12-34 mmSL']),
            {'found': True,
             'millimeters': [12, 34],
             'units_inferred': False,
             'regex': 'len_key_suffix',
             'field': 'col1',
             'start': 9,
             'end': 19,
             'key': 'SL'})

    def test_search_and_normalize_53(self):
        self.assertEqual(
            TARGET.search_and_normalize(['Measurements: L: 21.0 cm']),
            {'found': True,
             'millimeters': 210.0,
             'units_inferred': False,
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 0,
             'end': 24,
             'key': 'Measurements: L'})

    def test_search_and_normalize_54(self):
        self.assertEqual(
            TARGET.search_and_normalize(['SVL=44']),
            {'found': True,
             'millimeters': 44,
             'units_inferred': True,
             'regex': 'svl_len_key',
             'field': 'col1',
             'start': 0,
             'end': 6,
             'key': 'SVL'})

    def test_search_and_normalize55(self):
        # Disallow 0 length
        self.assertDictEqual(
            TARGET.search_and_normalize(['SVL=0 g']),
            {'found': False,
             'millimeters': None,
             'units_inferred': False,
             'regex': None,
             'field': None,
             'start': None,
             'end': None,
             'key': None})

    def test_search_and_normalize56(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['SVL=44', '', 'TL=50mm']),
            {'found': True,
             'millimeters': 50,
             'units_inferred': False,
             'regex': 'other_len_key',
             'field': 'col3',
             'start': 0,
             'end': 7,
             'key': 'TL'})

    def test_search_and_normalize57(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['TL=50', '', 'SVL=44mm']),
            {'found': True,
             'millimeters': 50,
             'units_inferred': True,
             'regex': 'other_len_key',
             'field': 'col1',
             'start': 0,
             'end': 5,
             'key': 'TL'})

    def test_search_and_normalize58(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['TgL=50', 'some other length', 'SVL=44mm']),
            {'found': True,
             'millimeters': 44,
             'units_inferred': False,
             'regex': 'svl_len_key',
             'field': 'col3',
             'start': 0,
             'end': 8,
             'key': 'SVL'})

    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    # The following are unresolved issues

    def test_search_and_normalize58a(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['unformatted measurements=42-51 mm SL', '', '']),
            {'found': True,
             'millimeters': [42, 51],
             'units_inferred': False,
             'regex': 'len_key_suffix',
             'field': 'col1',
             'start': 25,
             'end': 36,
             'key': 'SL'})

    def test_search_and_normalize59(self):
        # TODO: Maybe we should infer the units from other measurements?
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['SV 1.4, TAIL 1.0 CM. HATCHLING', '', '']),
            {'found': True,
             'millimeters': 1.4,
             'units_inferred': True,
             'regex': 'svl_len_key',
             'field': 'col1',
             'start': 0,
             'end': 6,
             'key': 'SV'})

    def test_search_and_normalize60(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['LENGTH 10 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN.', '']),
            {'found': True,
             'millimeters': 263.5,
             'units_inferred': False,
             'regex': 'len_fract',
             'field': 'col1',
             'start': 0,
             'end': 17,
             'key': 'LENGTH'})

    def test_search_and_normalize60a(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['LENGTH 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN.', '']),
            {'found': True,
             'millimeters': 9.5,
             'units_inferred': False,
             'regex': 'len_fract',
             'field': 'col1',
             'start': 0,
             'end': 14,
             'key': 'LENGTH'})

    def test_search_and_normalize60b(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['LENGTH 0 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN.', '']),
            {'found': True,
             'millimeters': 9.5,
             'units_inferred': False,
             'regex': 'len_fract',
             'field': 'col1',
             'start': 0,
             'end': 16,
             'key': 'LENGTH'})

    def test_search_and_normalize61(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                [('tail length in mm: -; total length in mm: -; '
                  'wing chord in mm: 81.0R; wing spread in mm: -'),
                 '',
                 '']),
            {'found': False,
             'millimeters': None,
             'units_inferred': False,
             'regex': None,
             'field': None,
             'start': None,
             'end': None,
             'key': None})

    def test_search_and_normalize62(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['76 cm S.L., 4.7 kg', '', '']),
            {'found': True,
             'millimeters': 760,
             'units_inferred': False,
             'regex': 'len_key_suffix',
             'field': 'col1',
             'start': 0,
             'end': 10,
             'key': 'S.L.'})

    def test_search_and_normalize63(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['set mark: 661 1-5 64-61', '', '']),
            {'found': False,
             'millimeters': None,
             'units_inferred': False,
             'regex': None,
             'field': None,
             'start': None,
             'end': None,
             'key': None})

    def test_search_and_normalize64(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['{"totalLength":"970", "wing":"390" }', 'L 970 mm', '']),
            {'found': True,
             'millimeters': 970,
             'units_inferred': True,
             'regex': 'total_len_key_num',
             'field': 'col1',
             'start': 2,
             'end': 19,
             'key': 'totalLength'})

    def test_search_and_normalize65(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['',
                 'SOURCE: M.A.CARRIKER JR.',
                 'LENGTH: 117MM. SOFT PARTS COLOR ON LABEL.']),
            {'found': True,
             'millimeters': 117,
             'units_inferred': False,
             'regex': 'len_key_ambiguous_units',
             'field': 'col3',
             'start': 0,
             'end': 14,
             'key': 'LENGTH'})

    def test_search_and_normalize66(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['Meas:Length (L): 5', '', '']),
            {'found': True,
             'millimeters': 5,
             'units_inferred': True,
             'regex': 'other_len_key',
             'field': 'col1',
             'start': 0,
             'end': 18,
             'key': 'Meas:Length (L)'})

    def test_search_and_normalize67(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['Size=41-148mm SL', '', '']),
            {'found': True,
             'millimeters': [41, 148],
             'units_inferred': False,
             'regex': 'len_key_suffix',
             'field': 'col1',
             'start': 5,
             'end': 16,
             'key': 'SL'})

    def test_search_and_normalize68(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['Size=105 mm TL, 87.1 mm PCL', '', '']),
            {'found': True,
             'millimeters': 105,
             'units_inferred': False,
             'regex': 'len_key_suffix',
             'field': 'col1',
             'start': 5,
             'end': 14,
             'key': 'TL'})

    def test_search_and_normalize69(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['Total Length: 185-252 mm', '', '']),
            {'found': True,
             'millimeters': [185, 252],
             'units_inferred': False,
             'regex': 'total_len_key',
             'field': 'col1',
             'start': 0,
             'end': 24,
             'key': 'Total Length'})

    def test_search_and_normalize70(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['Total Length: 185 - 252 mm', '', '']),
            {'found': True,
             'millimeters': [185, 252],
             'units_inferred': False,
             'regex': 'total_len_key',
             'field': 'col1',
             'start': 0,
             'end': 26,
             'key': 'Total Length'})

    def test_search_and_normalize71(self):
        # TODO This one is a trawl measurement of some kind, not an organism
        # measurement
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['{"time collected":"morning", "water depth":"9.1-18.3", '
                 '"bottom":"rock?", "length":"278" }', '', '']),
            {'found': True,
             'millimeters': 278,
             'units_inferred': True,
             'regex': 'len_key_ambiguous',
             'field': 'col1',
             'start': 73,
             'end': 86,
             'key': 'length'})


ARGS = Namespace(columns=['col1', 'col2', 'col3'])
TARGET = ParseTotalLength(ARGS)
SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(TestTotalLengthParser)
unittest.TextTestRunner().run(SUITE)
