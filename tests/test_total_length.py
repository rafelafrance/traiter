# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.trait_parsers.total_length import ParseTotalLength


class TestTotalLengthParser(unittest.TestCase):

    def test_parser_01(self):
        self.assertDictEqual(
            TARGET.parse('{"totalLengthInMM":"123" };'),
            {'key': 'totalLengthInMM',
             'value': '123',
             'regex': 'total_len_key_num',
             'units': 'MM'})

    def test_parser_02(self):
        self.assertDictEqual(
            TARGET.parse(
                'measurements: ToL=230;TaL=115;HF=22;E=18;'
                ' total length=230 mm; tail length=115 mm;'),
            {'key': 'total length',
             'value': '230',
             'regex': 'total_len_key_num',
             'units': 'mm'})

    def test_parser_03(self):
        self.assertEqual(
            TARGET.parse('sex=unknown ; crown-rump length=8 mm'),
            None)

    def test_parser_04(self):
        self.assertEqual(
            TARGET.parse('left gonad length=10 mm; right gonad length=10 mm;'),
            None)

    def test_parser_05(self):
        self.assertDictEqual(
            TARGET.parse('"{"measurements":"308-190-45-20" }"'),
            {'key': 'measurements',
             'value': '308',
             'regex': 'len_shorthand',
             'units': '_mm_'})

    def test_parser_06(self):
        self.assertDictEqual(
            TARGET.parse('308-190-45-20'),
            {'key': '_shorthand_',
             'value': '308',
             'regex': 'len_shorthand',
             'units': '_mm_'})

    def test_parser_07(self):
        self.assertDictEqual(
            TARGET.parse('{"measurements":"143-63-20-17=13 g" }'),
            {'key': 'measurements',
             'value': '143',
             'regex': 'len_shorthand',
             'units': '_mm_'})

    def test_parser_08(self):
        self.assertDictEqual(
            TARGET.parse('143-63-20-17=13'),
            {'key': '_shorthand_',
             'value': '143',
             'regex': 'len_shorthand',
             'units': '_mm_'})

    def test_parser_09(self):
        self.assertDictEqual(
            TARGET.parse(
                'snout-vent length=54 mm; total length=111 mm;'
                ' tail length=57 mm; weight=5 g'),
            {'key': 'total length',
             'value': '111',
             'regex': 'total_len_key_num',
             'units': 'mm'})

    def test_parser_10(self):
        self.assertDictEqual(
            TARGET.parse('unformatted measurements=Verbatim weight=X;'
                         'ToL=230;TaL=115;HF=22;E=18;'
                         ' total length=230 mm; tail length=115 mm;'),
            {'key': 'total length',
             'value': '230',
             'regex': 'total_len_key_num',
             'units': 'mm'})

    def test_parser_11(self):
        self.assertDictEqual(
            TARGET.parse('** Body length =345 cm; Blubber=1 cm '),
            {'key': 'Body length',
             'value': '345',
             'regex': 'other_len_key',
             'units': 'cm'})

    def test_parser_12(self):
        self.assertDictEqual(
            TARGET.parse('t.l.= 2 feet 3.1 - 4.5 inches '),
            {'key': 't.l.',
             'value': ['2', '3.1 - 4.5'],
             'regex': 'en_len',
             'units': ['feet', 'inches']})

    def test_parser_13(self):
        self.assertDictEqual(
            TARGET.parse('2 ft. 3.1 - 4.5 in. '),
            {'key': '_english_',
             'value': ['2', '3.1 - 4.5'],
             'regex': 'en_len',
             'units': ['ft.', 'in.']})

    def test_parser_14(self):
        self.assertDictEqual(
            TARGET.parse('total length= 2 ft.'),
            {'key': 'total length',
             'value': '2',
             'regex': 'total_len_key_num',
             'units': 'ft.'})

    def test_parser_15(self):
        self.assertDictEqual(
            TARGET.parse('AJR-32   186-102-23-15  15.0g'),
            {'key': '_shorthand_',
             'value': '186',
             'regex': 'len_shorthand',
             'units': '_mm_'})

    def test_parser_16(self):
        self.assertDictEqual(
            TARGET.parse('length=8 mm'),
            {'key': 'length',
             'value': '8',
             'regex': 'len_key_ambiguous_units',
             'units': 'mm'})

    def test_parser_17(self):
        self.assertDictEqual(
            TARGET.parse('another; length=8 mm'),
            {'key': 'length',
             'value': '8',
             'regex': 'len_key_ambiguous_units',
             'units': 'mm'})

    def test_parser_18(self):
        self.assertDictEqual(
            TARGET.parse('another; TL_120, noise'),
            {'key': 'TL_',
             'value': '120',
             'regex': 'other_len_key',
             'units': None})

    def test_parser_19(self):
        self.assertDictEqual(
            TARGET.parse('another; TL - 101.3mm, noise'),
            {'key': 'TL',
             'value': '101.3',
             'regex': 'other_len_key',
             'units': 'mm'})

    def test_parser_20(self):
        self.assertDictEqual(
            TARGET.parse('before; TL153, after'),
            {'key': 'TL',
             'value': '153',
             'regex': 'other_len_key',
             'units': None})

    def test_parser_21(self):
        self.assertDictEqual(
            TARGET.parse(
                'before; Total length in catalog and '
                'specimen tag as 117, after'),
            {'key': 'Total length',
             'value': '117',
             'regex': 'len_in_phrase',
             'units': None})

    def test_parser_22(self):
        self.assertDictEqual(
            TARGET.parse(
                'before Snout vent lengths range from 16 to 23 mm. after'),
            {'key': 'Snout vent lengths',
             'value': '16 to 23',
             'regex': 'len_in_phrase',
             'units': 'mm.'})

    def test_parser_23(self):
        self.assertDictEqual(
            TARGET.parse('Size=13 cm TL'),
            {'key': 'TL',
             'value': '13',
             'regex': 'len_key_suffix',
             'units': 'cm'})

    def test_parser_24(self):
        self.assertDictEqual(
            TARGET.parse('det_comments:31.5-58.3inTL'),
            {'key': 'TL',
             'value': '31.5-58.3',
             'regex': 'len_key_suffix',
             'units': 'in'})

    def test_parser_25(self):
        self.assertDictEqual(
            TARGET.parse('SVL52mm'),
            {'key': 'SVL',
             'value': '52',
             'regex': 'svl_len_key',
             'units': 'mm'})

    def test_parser_26(self):
        self.assertDictEqual(
            TARGET.parse(
                'snout-vent length=221 mm; total length=257 mm; '
                'tail length=36 mm'),
            {'key': 'total length',
             'value': '257',
             'regex': 'total_len_key_num',
             'units': 'mm'})

    def test_parser_27(self):
        self.assertDictEqual(
            TARGET.parse('SVL 209 mm, total 272 mm, 4.4 g.'),
            {'key': 'total',
             'value': '272',
             'regex': 'key_units_req',
             'units': 'mm'})

    def test_parser_28(self):
        self.assertDictEqual(
            TARGET.parse('{"time collected":"0712-0900", "length":"12.0" }'),
            {'key': 'length',
             'value': '12.0',
             'regex': 'len_key_ambiguous',
             'units': None})

    def test_parser_29(self):
        self.assertDictEqual(
            TARGET.parse('{"time collected":"1030", "water depth":"1-8", '
                         '"bottom":"abrupt lava '
                         'cliff dropping off to sand at 45 ft.", '
                         '"length":"119-137" }'),
            {'key': 'length',
             'value': '119-137',
             'regex': 'len_key_ambiguous',
             'units': None})

    def test_parser_30(self):
        self.assertDictEqual(
            TARGET.parse('TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx'),
            {'key': 'TL',
             'value': '44',
             'regex': 'len_key_abbrev',
             'units': 'mm'})

    def test_parser_31(self):
        self.assertDictEqual(
            TARGET.parse('{"totalLengthInMM":"270-165-18-22-31", '),
            {'key': 'totalLengthInMM',
             'value': '270',
             'regex': 'len_shorthand',
             'units': 'MM'})

    def test_parser_32(self):
        self.assertDictEqual(
            TARGET.parse('{"length":"20-29" }'),
            {'key': 'length',
             'value': '20-29',
             'regex': 'len_key_ambiguous',
             'units': None})

    def test_parser_33(self):
        self.assertDictEqual(
            TARGET.parse(
                'field measurements on fresh dead specimen '
                'were 157-60-20-19-21g'),
            {'key': '_shorthand_',
             'value': '157',
             'regex': 'len_shorthand',
             'units': '_mm_'})

    def test_parser_34(self):
        self.assertDictEqual(
            TARGET.parse('f age class: adult; standard length: 63-107mm'),
            {'key': 'standard length',
             'value': '63-107',
             'regex': 'total_len_key',
             'units': 'mm'})

    def test_parser_35(self):
        self.assertEqual(
            TARGET.parse('Rehydrated in acetic acid 7/1978-8/1987.'),
            None)

    def test_parser_36(self):
        self.assertDictEqual(
            TARGET.parse('age class: adult; standard length: 18.0-21.5mm'),
            {'key': 'standard length',
             'value': '18.0-21.5',
             'regex': 'total_len_key',
             'units': 'mm'})

    def test_parser_37(self):
        self.assertDictEqual(
            TARGET.parse('age class: adult; standard length: 18-21.5mm'),
            {'key': 'standard length',
             'value': '18-21.5',
             'regex': 'total_len_key',
             'units': 'mm'})

    def test_parser_38(self):
        self.assertDictEqual(
            TARGET.parse('age class: adult; standard length: 18.0-21mm'),
            {'key': 'standard length',
             'value': '18.0-21',
             'regex': 'total_len_key',
             'units': 'mm'})

    def test_parser_39(self):
        self.assertDictEqual(
            TARGET.parse('age class: adult; standard length: 18-21mm'),
            {'key': 'standard length',
             'value': '18-21',
             'regex': 'total_len_key',
             'units': 'mm'})

    def test_parser_40(self):
        self.assertEqual(
            TARGET.parse("Specimen #'s - 5491,5492,5498,5499,5505,5526,"
                         "5527,5528,5500,"
                         "5507,5508,5590,5592,5595,5594,5593,5596,5589,"
                         "5587,5586,5585"),
            None)

    def test_parser_41(self):
        self.assertEqual(
            TARGET.parse('20-28mm SL'),
            {'key': 'SL',
             'value': '20-28',
             'regex': 'len_key_suffix',
             'units': 'mm'})

    def test_parser_42(self):
        self.assertEqual(
            TARGET.parse('29mm SL'),
            {'key': 'SL',
             'value': '29',
             'regex': 'len_key_suffix',
             'units': 'mm'})

    def test_parser_43(self):
        self.assertEqual(
            TARGET.parse('{"measurements":"159-?-22-16=21.0" }'),
            {'key': 'measurements',
             'value': '159',
             'regex': 'len_shorthand',
             'units': '_mm_'})

    def test_parser_44(self):
        self.assertEqual(
            TARGET.parse('c701563b-dbd9-4500-184f-1ad61eb8da11'),
            None)

    def test_parser_45(self):
        self.assertEqual(
            TARGET.parse('Meas: L: 21.0'),
            {'key': 'Meas: L',
             'value': '21.0',
             'regex': 'total_len_key_num',
             'units': '_mm_'})

    def test_parser_46(self):
        self.assertEqual(
            TARGET.parse('Meas: L: 21.0 cm'),
            {'key': 'Meas: L',
             'value': '21.0',
             'regex': 'total_len_key_num',
             'units': 'cm'})

    def test_parser_47(self):
        self.assertEqual(
            TARGET.parse('LABEL. LENGTH 375 MM.'),
            {'key': 'LABEL. LENGTH',
             'value': '375',
             'regex': 'total_len_key_num',
             'units': 'MM.'})

    def test_parser_48(self):
        self.assertEqual(
            TARGET.parse('SL=12mm'),
            {'key': 'SL',
             'value': '12',
             'regex': 'total_len_key_num',
             'units': 'mm'})

    def test_parser_49(self):
        self.assertEqual(
            TARGET.parse('Size=SL 12-14 mm'),
            {'key': 'SL',
             'value': '12-14',
             'regex': 'total_len_key',
             'units': 'mm'})

    def test_parser_50(self):
        self.assertEqual(
            TARGET.parse('SV 1.2'),
            {'key': 'SV',
             'value': '1.2',
             'regex': 'svl_len_key',
             'units': None})

    def test_parser_51(self):
        self.assertEqual(
            TARGET.parse(' Length: 123 mm SL'),
            {'key': 'SL',
             'value': '123',
             'regex': 'len_key_suffix',
             'units': 'mm'})

    def test_parser_52(self):
        self.assertEqual(
            TARGET.parse(' Length: 12-34 mmSL'),
            {'key': 'SL',
             'value': '12-34',
             'regex': 'len_key_suffix',
             'units': 'mm'})

    def test_parser_53(self):
        self.assertEqual(
            TARGET.parse('Measurements: L: 21.0 cm'),
            {'key': 'Measurements: L',
             'value': '21.0',
             'regex': 'total_len_key_num',
             'units': 'cm'})

    def test_parser_54(self):
        self.assertEqual(
            TARGET.parse('SVL=44'),
            {'key': 'SVL',
             'value': '44',
             'regex': 'svl_len_key',
             'units': None})

    def test_parser_55(self):
        self.assertDictEqual(
            TARGET.parse('Total Length: 185 - 252 mm'),
            {'key': 'Total Length',
             'regex': 'total_len_key',
             'value': '185 - 252',
             'units': 'mm'})

    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################

    def test_search_and_normalize_01(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['{"totalLengthInMM":"123" };']),
            {'has_length': True,
             'length_in_mm': 123,
             'length_units_inferred': False,
             'regex': 'total_len_key_num',
             'key': 'totalLengthInMM'})

    def test_search_and_normalize_02(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['measurements: ToL=230;TaL=115;HF=22;E=18; total '
                 'length=230 mm; tail length=115 mm;']),
            {'has_length': True,
             'length_in_mm': 230,
             'length_units_inferred': False,
             'regex': 'total_len_key_num',
             'key': 'total length'})

    def test_search_and_normalize_03(self):
        self.assertEqual(
            TARGET.search_and_normalize(
                ['sex=unknown ; crown-rump length=8 mm']),
            {'has_length': False,
             'length_in_mm': None,
             'length_units_inferred': False,
             'regex': None,
             'key': None})

    def test_search_and_normalize_04(self):
        self.assertEqual(
            TARGET.search_and_normalize(
                ['left gonad length=10 mm; right gonad length=10 mm;']),
            {'has_length': False,
             'length_in_mm': None,
             'length_units_inferred': False,
             'regex': None,
             'key': None})

    def test_search_and_normalize_05(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['"{"measurements":"308-190-45-20" }"']),
            {'has_length': True,
             'length_in_mm': 308,
             'length_units_inferred': True,
             'regex': 'len_shorthand',
             'key': 'measurements'})

    def test_search_and_normalize_06(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['308-190-45-20']),
            {'has_length': True,
             'length_in_mm': 308,
             'length_units_inferred': True,
             'regex': 'len_shorthand',
             'key': '_shorthand_'})

    def test_search_and_normalize_07(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['{"measurements":"143-63-20-17=13 g" }']),
            {'has_length': True,
             'length_in_mm': 143,
             'length_units_inferred': True,
             'regex': 'len_shorthand',
             'key': 'measurements'})

    def test_search_and_normalize_08(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['143-63-20-17=13']),
            {'has_length': True,
             'length_in_mm': 143,
             'length_units_inferred': True,
             'regex': 'len_shorthand',
             'key': '_shorthand_'})

    def test_search_and_normalize_09(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['snout-vent length=54 mm; total length=111 mm; '
                 'tail length=57 mm; weight=5 g']),
            {'has_length': True,
             'length_in_mm': 111,
             'length_units_inferred': False,
             'regex': 'total_len_key_num',
             'key': 'total length'})

    def test_search_and_normalize_10(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['unformatted measurements=Verbatim weight=X;ToL=230;TaL=115;'
                 'HF=22;E=18; total length=230 mm; tail length=115 mm;']),
            {'has_length': True,
             'length_in_mm': 230,
             'length_units_inferred': False,
             'regex': 'total_len_key_num',
             'key': 'total length'})

    def test_search_and_normalize_11(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['** Body length =345 cm; Blubber=1 cm ']),
            {'has_length': True,
             'length_in_mm': 3450,
             'length_units_inferred': False,
             'regex': 'other_len_key',
             'key': 'Body length'})

    def test_search_and_normalize_12(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['t.l.= 2 feet 3.1 - 4.5 inches ']),
            {'has_length': True,
             'length_in_mm': [688.7, 724.3],
             'length_units_inferred': False,
             'regex': 'en_len',
             'key': 't.l.'})

    def test_search_and_normalize_13(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['2 ft. 3.1 - 4.5 in. ']),
            {'has_length': True,
             'length_in_mm': [688.7, 724.3],
             'length_units_inferred': False,
             'regex': 'en_len',
             'key': '_english_'})

    def test_search_and_normalize_14(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['total length= 2 ft.']),
            {'has_length': True,
             'length_in_mm': 610,
             'length_units_inferred': False,
             'regex': 'total_len_key_num',
             'key': 'total length'})

    def test_search_and_normalize_15(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['AJR-32   186-102-23-15  15.0g']),
            {'has_length': True,
             'length_in_mm': 186,
             'length_units_inferred': True,
             'regex': 'len_shorthand',
             'key': '_shorthand_'})

    def test_search_and_normalize_16(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['length=8 mm']),
            {'has_length': True,
             'length_in_mm': 8,
             'length_units_inferred': False,
             'regex': 'len_key_ambiguous_units',
             'key': 'length'})

    def test_search_and_normalize_17(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['another; length=8 mm']),
            {'has_length': True,
             'length_in_mm': 8,
             'length_units_inferred': False,
             'regex': 'len_key_ambiguous_units',
             'key': 'length'})

    def test_search_and_normalize_18(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['another; TL_120, noise']),
            {'has_length': True,
             'length_in_mm': 120,
             'length_units_inferred': True,
             'regex': 'other_len_key',
             'key': 'TL_'})

    def test_search_and_normalize_19(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['another; TL - 101.3mm, noise']),
            {'has_length': True,
             'length_in_mm': 101.3,
             'length_units_inferred': False,
             'regex': 'other_len_key',
             'key': 'TL'})

    def test_search_and_normalize_20(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['before; TL153, after']),
            {'has_length': True,
             'length_in_mm': 153,
             'length_units_inferred': True,
             'regex': 'other_len_key',
             'key': 'TL'})

    def test_search_and_normalize_21(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['before; Total length in catalog and specimen tag as '
                 '117, after']),
            {'has_length': True,
             'length_in_mm': 117,
             'length_units_inferred': True,
             'regex': 'len_in_phrase',
             'key': 'Total length'})

    def test_search_and_normalize_22(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['before Snout vent lengths range from 16 to 23 mm. after']),
            {'has_length': True,
             'length_in_mm': [16, 23],
             'length_units_inferred': False,
             'regex': 'len_in_phrase',
             'key': 'Snout vent lengths'})

    def test_search_and_normalize_23(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['Size=13 cm TL']),
            {'has_length': True,
             'length_in_mm': 130,
             'length_units_inferred': False,
             'regex': 'len_key_suffix',
             'key': 'TL'})

    def test_search_and_normalize_24(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['det_comments:31.5-58.3inTL']),
            {'has_length': True,
             'length_in_mm': [800.1, 1480.8],
             'length_units_inferred': False,
             'regex': 'len_key_suffix',
             'key': 'TL'})

    def test_search_and_normalize_25(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['SVL52mm']),
            {'has_length': True,
             'length_in_mm': 52,
             'length_units_inferred': False,
             'regex': 'svl_len_key',
             'key': 'SVL'})

    def test_search_and_normalize_26(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['snout-vent length=221 mm; total length=257 mm; '
                 'tail length=36 mm']),
            {'has_length': True,
             'length_in_mm': 257,
             'length_units_inferred': False,
             'regex': 'total_len_key_num',
             'key': 'total length'})

    def test_search_and_normalize_27(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['SVL 209 mm, total 272 mm, 4.4 g.']),
            {'has_length': True,
             'length_in_mm': 272,
             'length_units_inferred': False,
             'regex': 'key_units_req',
             'key': 'total'})

    def test_search_and_normalize_28(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['{"time collected":"0712-0900", "length":"12.0" }']),
            {'has_length': True,
             'length_in_mm': 12.0,
             'length_units_inferred': True,
             'regex': 'len_key_ambiguous',
             'key': 'length'})

    def test_search_and_normalize_29(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['{"time collected":"1030", "water depth":"1-8", '
                 '"bottom":"abrupt lava cliff dropping off to sand at '
                 '45 ft.", "length":"119-137" }']),
            {'has_length': True,
             'length_in_mm': [119, 137],
             'length_units_inferred': True,
             'regex': 'len_key_ambiguous',
             'key': 'length'})

    def test_search_and_normalize_30(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx']),
            {'has_length': True,
             'length_in_mm': 44,
             'length_units_inferred': False,
             'regex': 'len_key_abbrev',
             'key': 'TL'})

    def test_search_and_normalize_31(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['{"totalLengthInMM":"270-165-18-22-31", ']),
            {'has_length': True,
             'length_in_mm': 270,
             'length_units_inferred': False,
             'regex': 'len_shorthand',
             'key': 'totalLengthInMM'})

    def test_search_and_normalize_32(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['{"length":"20-29" }']),
            {'has_length': True,
             'length_in_mm': [20, 29],
             'length_units_inferred': True,
             'regex': 'len_key_ambiguous',
             'key': 'length'})

    def test_search_and_normalize_33(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['field measurements on fresh dead specimen were '
                 '157-60-20-19-21g']),
            {'has_length': True,
             'length_in_mm': 157,
             'length_units_inferred': True,
             'regex': 'len_shorthand',
             'key': '_shorthand_'})

    def test_search_and_normalize_34(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['f age class: adult; standard length: 63-107mm']),
            {'has_length': True,
             'length_in_mm': [63, 107],
             'length_units_inferred': False,
             'regex': 'total_len_key',
             'key': 'standard length'})

    def test_search_and_normalize_35(self):
        self.assertEqual(
            TARGET.search_and_normalize(
                ['Rehydrated in acetic acid 7/1978-8/1987.']),
            {'has_length': False,
             'length_in_mm': None,
             'length_units_inferred': False,
             'regex': None,
             'key': None})

    def test_search_and_normalize_36(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['age class: adult; standard length: 18.0-21.5mm']),
            {'has_length': True,
             'length_in_mm': [18.0, 21.5],
             'length_units_inferred': False,
             'regex': 'total_len_key',
             'key': 'standard length'})

    def test_search_and_normalize_37(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['age class: adult; standard length: 18-21.5mm']),
            {'has_length': True,
             'length_in_mm': [18, 21.5],
             'length_units_inferred': False,
             'regex': 'total_len_key',
             'key': 'standard length'})

    def test_search_and_normalize_38(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['age class: adult; standard length: 18.0-21mm']),
            {'has_length': True,
             'length_in_mm': [18.0, 21],
             'length_units_inferred': False,
             'regex': 'total_len_key',
             'key': 'standard length'})

    def test_search_and_normalize_39(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['age class: adult; standard length: 18-21mm']),
            {'has_length': True,
             'length_in_mm': [18, 21],
             'length_units_inferred': False,
             'regex': 'total_len_key',
             'key': 'standard length'})

    def test_search_and_normalize_40(self):
        self.assertEqual(
            TARGET.search_and_normalize(
                "Specimen #'s - 5491,5492,5498,5499,5505,5526,5527,5528,5500,"
                "5507,5508,5590,5592,5595,5594,5593,5596,5589,5587,5586,5585"),
            {'has_length': False,
             'length_in_mm': None,
             'length_units_inferred': False,
             'regex': None,
             'key': None})

    def test_search_and_normalize_41(self):
        self.assertEqual(
            TARGET.search_and_normalize(['20-28mm SL']),
            {'has_length': True,
             'length_in_mm': [20, 28],
             'length_units_inferred': False,
             'regex': 'len_key_suffix',
             'key': 'SL'})

    def test_search_and_normalize_42(self):
        self.assertEqual(
            TARGET.search_and_normalize(['29mm SL']),
            {'has_length': True,
             'length_in_mm': 29,
             'length_units_inferred': False,
             'regex': 'len_key_suffix',
             'key': 'SL'})

    def test_search_and_normalize_43(self):
        self.assertEqual(
            TARGET.search_and_normalize(
                ['{"measurements":"159-?-22-16=21.0" }']),
            {'has_length': True,
             'length_in_mm': 159,
             'length_units_inferred': True,
             'regex': 'len_shorthand',
             'key': 'measurements'})

    def test_search_and_normalize_44(self):
        self.assertEqual(
            TARGET.search_and_normalize(
                ['c701563b-dbd9-4500-184f-1ad61eb8da11']),
            {'has_length': False,
             'length_in_mm': None,
             'length_units_inferred': False,
             'regex': None,
             'key': None})

    def test_search_and_normalize_45(self):
        self.assertEqual(
            TARGET.search_and_normalize(['Meas: L: 21.0']),
            {'has_length': True,
             'length_in_mm': 21.0,
             'length_units_inferred': True,
             'regex': 'total_len_key_num',
             'key': 'Meas: L'})

    def test_search_and_normalize_46(self):
        self.assertEqual(
            TARGET.search_and_normalize(['Meas: L: 21.0 cm']),
            {'has_length': True,
             'length_in_mm': 210.0,
             'length_units_inferred': False,
             'regex': 'total_len_key_num',
             'key': 'Meas: L'})

    def test_search_and_normalize_47(self):
        self.assertEqual(
            TARGET.search_and_normalize(['LABEL. LENGTH 375 MM.']),
            {'has_length': True,
             'length_in_mm': 375,
             'length_units_inferred': False,
             'regex': 'total_len_key_num',
             'key': 'LABEL. LENGTH'})

    def test_search_and_normalize_48(self):
        self.assertEqual(
            TARGET.search_and_normalize(['SL=12mm']),
            {'has_length': True,
             'length_in_mm': 12,
             'length_units_inferred': False,
             'regex': 'total_len_key_num',
             'key': 'SL'})

    def test_search_and_normalize_49(self):
        self.assertEqual(
            TARGET.search_and_normalize(['Size=SL 12-14 mm']),
            {'has_length': True,
             'length_in_mm': [12, 14],
             'length_units_inferred': False,
             'regex': 'total_len_key',
             'key': 'SL'})

    def test_search_and_normalize_50(self):
        self.assertEqual(
            TARGET.search_and_normalize(['SV 1.2']),
            {'has_length': True,
             'length_in_mm': 1.2,
             'length_units_inferred': True,
             'regex': 'svl_len_key',
             'key': 'SV'})

    def test_search_and_normalize_51(self):
        self.assertEqual(
            TARGET.search_and_normalize([' Length: 123 mm SL']),
            {'has_length': True,
             'length_in_mm': 123,
             'length_units_inferred': False,
             'regex': 'len_key_suffix',
             'key': 'SL'})

    def test_search_and_normalize_52(self):
        self.assertEqual(
            TARGET.search_and_normalize([' Length: 12-34 mmSL']),
            {'has_length': True,
             'length_in_mm': [12, 34],
             'length_units_inferred': False,
             'regex': 'len_key_suffix',
             'key': 'SL'})

    def test_search_and_normalize_53(self):
        self.assertEqual(
            TARGET.search_and_normalize(['Measurements: L: 21.0 cm']),
            {'has_length': True,
             'length_in_mm': 210.0,
             'length_units_inferred': False,
             'regex': 'total_len_key_num',
             'key': 'Measurements: L'})

    def test_search_and_normalize_54(self):
        self.assertEqual(
            TARGET.search_and_normalize(['SVL=44']),
            {'has_length': True,
             'length_in_mm': 44,
             'length_units_inferred': True,
             'regex': 'svl_len_key',
             'key': 'SVL'})

    def test_search_and_normalize55(self):
        # Disallow 0 length
        self.assertDictEqual(
            TARGET.search_and_normalize(['SVL=0 g']),
            {'has_length': False,
             'length_in_mm': None,
             'length_units_inferred': False,
             'regex': None,
             'key': None})

    def test_search_and_normalize56(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['SVL=44', '', 'TL=50mm']),
            {'has_length': True,
             'length_in_mm': 50,
             'length_units_inferred': False,
             'regex': 'other_len_key',
             'key': 'TL'})

    def test_search_and_normalize57(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['TL=50', '', 'SVL=44mm']),
            {'has_length': True,
             'length_in_mm': 50,
             'length_units_inferred': True,
             'regex': 'other_len_key',
             'key': 'TL'})

    def test_search_and_normalize58(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['TgL=50', 'some other length', 'SVL=44mm']),
            {'has_length': True,
             'length_in_mm': 44,
             'length_units_inferred': False,
             'regex': 'svl_len_key',
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
            {'has_length': True,
             'length_in_mm': [42, 51],
             'length_units_inferred': False,
             'regex': 'len_key_suffix',
             'key': 'SL'})

    def test_search_and_normalize59(self):
        # TODO: Maybe we should infer the units from other measurements?
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['SV 1.4, TAIL 1.0 CM. HATCHLING', '', '']),
            {'has_length': True,
             'length_in_mm': 1.4,
             'length_units_inferred': True,
             'regex': 'svl_len_key',
             'key': 'SV'})

    def test_search_and_normalize60(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['LENGTH 10 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN.', '']),
            {'has_length': True,
             'length_in_mm': 263.5,
             'length_units_inferred': False,
             'regex': 'len_fract',
             'key': 'LENGTH'})

    def test_search_and_normalize60a(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['LENGTH 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN.', '']),
            {'has_length': True,
             'length_in_mm': 9.5,
             'length_units_inferred': False,
             'regex': 'len_fract',
             'key': 'LENGTH'})

    def test_search_and_normalize60b(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['LENGTH 0 3/8 IN. WING CHORD 5.25 IN. TAIL 4.25 IN.', '']),
            {'has_length': True,
             'length_in_mm': 9.5,
             'length_units_inferred': False,
             'regex': 'len_fract',
             'key': 'LENGTH'})

    def test_search_and_normalize61(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                [('tail length in mm: -; total length in mm: -; '
                  'wing chord in mm: 81.0R; wing spread in mm: -'),
                 '',
                 '']),
            {'has_length': False,
             'length_in_mm': None,
             'length_units_inferred': False,
             'regex': None,
             'key': None})

    def test_search_and_normalize62(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['76 cm S.L., 4.7 kg', '', '']),
            {'has_length': True,
             'length_in_mm': 760,
             'length_units_inferred': False,
             'regex': 'len_key_suffix',
             'key': 'S.L.'})

    def test_search_and_normalize63(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['set mark: 661 1-5 64-61', '', '']),
            {'has_length': False,
             'length_in_mm': None,
             'length_units_inferred': False,
             'regex': None,
             'key': None})

    def test_search_and_normalize64(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['{"totalLength":"970", "wing":"390" }', 'L 970 mm', '']),
            {'has_length': True,
             'length_in_mm': 970,
             'length_units_inferred': True,
             'regex': 'total_len_key_num',
             'key': 'totalLength'})

    def test_search_and_normalize65(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['',
                 'SOURCE: M.A.CARRIKER JR.',
                 'LENGTH: 117MM. SOFT PARTS COLOR ON LABEL.']),
            {'has_length': True,
             'length_in_mm': 117,
             'length_units_inferred': False,
             'regex': 'len_key_ambiguous_units',
             'key': 'LENGTH'})

    def test_search_and_normalize66(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['Meas:Length (L): 5', '', '']),
            {'has_length': True,
             'length_in_mm': 5,
             'length_units_inferred': True,
             'regex': 'other_len_key',
             'key': 'Meas:Length (L)'})

    def test_search_and_normalize67(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['Size=41-148mm SL', '', '']),
            {'has_length': True,
             'length_in_mm': [41, 148],
             'length_units_inferred': False,
             'regex': 'len_key_suffix',
             'key': 'SL'})

    def test_search_and_normalize68(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['Size=105 mm TL, 87.1 mm PCL', '', '']),
            {'has_length': True,
             'length_in_mm': 105,
             'length_units_inferred': False,
             'regex': 'len_key_suffix',
             'key': 'TL'})

    def test_search_and_normalize69(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['Total Length: 185-252 mm', '', '']),
            {'has_length': True,
             'length_in_mm': [185, 252],
             'length_units_inferred': False,
             'regex': 'total_len_key',
             'key': 'Total Length'})

    def test_search_and_normalize70(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['Total Length: 185 - 252 mm', '', '']),
            {'has_length': True,
             'length_in_mm': [185, 252],
             'length_units_inferred': False,
             'regex': 'total_len_key',
             'key': 'Total Length'})

    def test_search_and_normalize71(self):
        # TODO This one is a trawl measurement of some kind, not an organism
        # measurement
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['{"time collected":"morning", "water depth":"9.1-18.3", '
                 '"bottom":"rock?", "length":"278" }', '', '']),
            {'has_length': True,
             'length_in_mm': 278,
             'length_units_inferred': True,
             'regex': 'len_key_ambiguous',
             'key': 'length'})


TARGET = ParseTotalLength()
SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(TestTotalLengthParser)
unittest.TextTestRunner().run(SUITE)
