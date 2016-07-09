#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The line above is to signify that the script contains utf-8 encoded characters.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Adapted from https://github.com/rafelafrance/traiter

__author__ = "John Wieczorek"
__contributors__ = "Raphael LaFrance, John Wieczorek"
__copyright__ = "Copyright 2016 vertnet.org"
__version__ = "test_total_length_parser.py 2016-07-08T09:14+02:00"

import unittest
from trait_parsers.total_length_parser import TotalLengthParser


class TestTotalLengthParser(unittest.TestCase):

    def test_parser_1(self):
        self.assertDictEqual(
            target.parse('{"totalLengthInMM":"123" };'),
            {'key': 'totalLengthInMM', 'value': '123', 'units': 'MM'})

    def test_parser_2(self):
        self.assertDictEqual(
            target.parse('measurements: ToL=230;TaL=115;HF=22;E=18; total length=230 mm; tail length=115 mm;'),
            {'key': 'total length', 'value': '230', 'units': 'mm'})

    def test_parser_3(self):
        self.assertEqual(
            target.parse('sex=unknown ; crown-rump length=8 mm'),
            None)

    def test_parser_4(self):
        self.assertEqual(
            target.parse('left gonad length=10 mm; right gonad length=10 mm;'),
            None)

    def test_parser_5(self):
        self.assertDictEqual(
            target.parse('"{"measurements":"308-190-45-20" }"'),
            {'key': 'measurements', 'value': '308', 'units': '_mm_'})

    def test_parser_6(self):
        self.assertDictEqual(
            target.parse('308-190-45-20'),
            {'key': '_shorthand_', 'value': '308', 'units': '_mm_'})

    def test_parser_7(self):
        self.assertDictEqual(
            target.parse('{"measurements":"143-63-20-17=13 g" }'),
            {'key': 'measurements', 'value': '143', 'units': '_mm_'})

    def test_parser_8(self):
        self.assertDictEqual(
            target.parse('143-63-20-17=13'),
            {'key': '_shorthand_', 'value': '143', 'units': '_mm_'})

    def test_parser_9(self):
        self.assertDictEqual(
            target.parse('snout-vent length=54 mm; total length=111 mm; tail length=57 mm; weight=5 g'),
            {'key': 'total length', 'value': '111', 'units': 'mm'})

    def test_parser_10(self):
        self.assertDictEqual(
            target.parse('unformatted measurements=Verbatim weight=X;ToL=230;TaL=115;HF=22;E=18;'
                         ' total length=230 mm; tail length=115 mm;'),
            {'key': 'total length', 'value': '230', 'units': 'mm'})

    def test_parser_11(self):
        self.assertDictEqual(
            target.parse('** Body length =345 cm; Blubber=1 cm '),
            {'key': 'Body length', 'value': '345', 'units': 'cm'})

    def test_parser_12(self):
        self.assertDictEqual(
            target.parse('t.l.= 2 feet 3.1 - 4.5 inches '),
            {'key': 't.l.', 'value': ['2', '3.1 - 4.5'], 'units': ['feet', 'inches']})

    def test_parser_13(self):
        self.assertDictEqual(
            target.parse('2 ft. 3.1 - 4.5 in. '),
            {'key': '_english_', 'value': ['2', '3.1 - 4.5'], 'units': ['ft.', 'in.']})

    def test_parser_14(self):
        self.assertDictEqual(
            target.parse('total length= 2 ft.'),
            {'key': 'total length', 'value': '2', 'units': 'ft.'})

    def test_parser_15(self):
        self.assertDictEqual(
            target.parse('AJR-32   186-102-23-15  15.0g'),
            {'key': '_shorthand_', 'value': '186', 'units': '_mm_'})

    def test_parser_16(self):
        self.assertDictEqual(
            target.parse('length=8 mm'),
            {'key': 'length', 'value': '8', 'units': 'mm'})

    def test_parser_17(self):
        self.assertDictEqual(
            target.parse('another; length=8 mm'),
            {'key': 'length', 'value': '8', 'units': 'mm'})

    def test_parser_18(self):
        self.assertDictEqual(
            target.parse('another; TL_120, noise'),
            {'key': 'TL_', 'value': '120', 'units': None})

    def test_parser_19(self):
        self.assertDictEqual(
            target.parse('another; TL - 101.3mm, noise'),
            {'key': 'TL', 'value': '101.3', 'units': 'mm'})

    def test_parser_20(self):
        self.assertDictEqual(
            target.parse('before; TL153, after'),
            {'key': 'TL', 'value': '153', 'units': None})

    def test_parser_21(self):
        self.assertDictEqual(
            target.parse('before; Total length in catalog and specimen tag as 117, after'),
            {'key': 'Total length', 'value': '117', 'units': None})

    def test_parser_22(self):
        self.assertDictEqual(
            target.parse('before Snout vent lengths range from 16 to 23 mm. after'),
            {'key': 'Snout vent lengths', 'value': '16 to 23', 'units': 'mm.'})

    def test_parser_23(self):
        self.assertDictEqual(
            target.parse('Size=13 cm TL'),
            {'key': 'TL', 'value': '13', 'units': 'cm'})

    def test_parser_24(self):
        self.assertDictEqual(
            target.parse('det_comments:31.5-58.3inTL'),
            {'key': 'TL', 'value': '31.5-58.3', 'units': 'in'})

    def test_parser_25(self):
        self.assertDictEqual(
            target.parse('SVL52mm'),
            {'key': 'SVL', 'value': '52', 'units': 'mm'})

    def test_parser_26(self):
        self.assertDictEqual(
            target.parse('snout-vent length=221 mm; total length=257 mm; tail length=36 mm'),
            {'key': 'total length', 'value': '257', 'units': 'mm'})

    def test_parser_27(self):
        self.assertDictEqual(
            target.parse('SVL 209 mm, total 272 mm, 4.4 g.'),
            {'key': 'total', 'value': '272', 'units': 'mm'})

    def test_parser_28(self):
        self.assertDictEqual(
            target.parse('{"time collected":"0712-0900", "length":"12.0" }'),
            {'key': 'length', 'value': '12.0', 'units': None})

    def test_parser_29(self):
        self.assertDictEqual(
            target.parse('{"time collected":"1030", "water depth":"1-8", "bottom":"abrupt lava '
                         'cliff dropping off to sand at 45 ft.", "length":"119-137" }'),
            {'key': 'length', 'value': '119-137', 'units': None})

    def test_parser_30(self):
        self.assertDictEqual(
            target.parse('TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx'),
            {'key': 'TL', 'value': '44', 'units': 'mm'})

    def test_parser_31(self):
        self.assertDictEqual(
            target.parse('{"totalLengthInMM":"270-165-18-22-31", '),
            {'key': 'totalLengthInMM', 'value': '270', 'units': 'MM'})

    def test_parser_32(self):
        self.assertDictEqual(
            target.parse('{"length":"20-29" }'),
            {'key': 'length', 'value': '20-29', 'units': None})

    def test_parser_33(self):
        self.assertDictEqual(
            target.parse('field measurements on fresh dead specimen were 157-60-20-19-21g'),
            {'key': '_shorthand_', 'value': '157', 'units': '_mm_'})

    def test_parser_34(self):
        self.assertDictEqual(
            target.parse('f age class: adult; standard length: 63-107mm'),
            {'key': 'standard length', 'value': '63-107', 'units': 'mm'})

    def test_parser_35(self):
        self.assertEqual(
            target.parse('Rehydrated in acetic acid 7/1978-8/1987.'),
            None)

    def test_parser_36(self):
        self.assertDictEqual(
            target.parse('age class: adult; standard length: 18.0-21.5mm'),
            {'key': 'standard length', 'value': '18.0-21.5', 'units': 'mm'})

    def test_parser_37(self):
        self.assertDictEqual(
            target.parse('age class: adult; standard length: 18-21.5mm'),
            {'key': 'standard length', 'value': '18-21.5', 'units': 'mm'})

    def test_parser_38(self):
        self.assertDictEqual(
            target.parse('age class: adult; standard length: 18.0-21mm'),
            {'key': 'standard length', 'value': '18.0-21', 'units': 'mm'})

    def test_parser_39(self):
        self.assertDictEqual(
            target.parse('age class: adult; standard length: 18-21mm'),
            {'key': 'standard length', 'value': '18-21', 'units': 'mm'})

    def test_parser_40(self):
        self.assertEqual(
            target.parse("Specimen #'s - 5491,5492,5498,5499,5505,5526,5527,5528,5500,"
                         "5507,5508,5590,5592,5595,5594,5593,5596,5589,5587,5586,5585"),
            None)

    def test_parser_41(self):
        self.assertEqual(
            target.parse('20-28mm SL'),
            {'key': 'SL', 'value': '20-28', 'units': 'mm'})

    def test_parser_42(self):
        self.assertEqual(
            target.parse('29mm SL'),
            {'key': 'SL', 'value': '29', 'units': 'mm'})

    def test_parser_43(self):
        self.assertEqual(
            target.parse('{"measurements":"159-?-22-16=21.0" }'),
            {'key': 'measurements', 'value': '159', 'units': '_mm_'})

    def test_parser_44(self):
        self.assertEqual(
            target.parse('c701563b-dbd9-4500-184f-1ad61eb8da11'),
            None)

    def test_parser_45(self):
        self.assertEqual(
            target.parse('Meas: L: 21.0'),
            {'key': 'Meas: L', 'value': '21.0', 'units': '_mm_'})

    def test_parser_46(self):
        self.assertEqual(
            target.parse('Meas: L: 21.0 cm'),
            {'key': 'Meas: L', 'value': '21.0', 'units': 'cm'})

    def test_parser_47(self):
        self.assertEqual(
            target.parse('LABEL. LENGTH 375 MM.'),
            {'key': 'LABEL. LENGTH', 'value': '375', 'units': 'MM.'})

    def test_parser_48(self):
        self.assertEqual(
            target.parse('SL=12mm'),
            {'key': 'SL', 'value': '12', 'units': 'mm'})

    def test_parser_49(self):
        self.assertEqual(
            target.parse('Size=SL 12-14 mm'),
            {'key': 'SL', 'value': '12-14', 'units': 'mm'})

    def test_parser_50(self):
        self.assertEqual(
            target.parse('SV 1.2'),
            {'key': 'SV', 'value': '1.2', 'units': None})

    def test_parser_51(self):
        self.assertEqual(
            target.parse(' Length: 123 mm SL'),
            {'key': 'SL', 'value': '123', 'units': 'mm'})

    def test_parser_52(self):
        self.assertEqual(
            target.parse(' Length: 12-34 mmSL'),
            {'key': 'SL', 'value': '12-34', 'units': 'mm'})

    def test_parser_53(self):
        self.assertEqual(
            target.parse('Measurements: L: 21.0 cm'),
            {'key': 'Measurements: L', 'value': '21.0', 'units': 'cm'})

    def test_parser_54(self):
        self.assertEqual(
            target.parse('SVL=44'),
            {'key': 'SVL', 'value': '44', 'units': None})

    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################

    def test_search_and_normalize_1(self):
        self.assertDictEqual(
            target.search_and_normalize(['{"totalLengthInMM":"123" };']),
            {'haslength': 1, 'lengthinmm': 123, 'lengthunitsinferred': 0})

    def test_search_and_normalize_2(self):
        self.assertDictEqual(
            target.search_and_normalize(['measurements: ToL=230;TaL=115;HF=22;E=18; total length=230 mm; tail length=115 mm;']),
            {'haslength': 1, 'lengthinmm': 230, 'lengthunitsinferred': 0})

    def test_search_and_normalize_3(self):
        self.assertEqual(
            target.search_and_normalize(['sex=unknown ; crown-rump length=8 mm']),
            {'lengthinmm': None, 'haslength': 0, 'lengthunitsinferred': None})

    def test_search_and_normalize_4(self):
        self.assertEqual(
            target.search_and_normalize(['left gonad length=10 mm; right gonad length=10 mm;']),
            {'lengthinmm': None, 'haslength': 0, 'lengthunitsinferred': None})

    def test_search_and_normalize_5(self):
        self.assertDictEqual(
            target.search_and_normalize(['"{"measurements":"308-190-45-20" }"']),
            {'haslength': 1, 'lengthinmm': 308, 'lengthunitsinferred': 1})

    def test_search_and_normalize_6(self):
        self.assertDictEqual(
            target.search_and_normalize(['308-190-45-20']),
            {'haslength': 1, 'lengthinmm': 308, 'lengthunitsinferred': 1})

    def test_search_and_normalize_7(self):
        self.assertDictEqual(
            target.search_and_normalize(['{"measurements":"143-63-20-17=13 g" }']),
            {'haslength': 1, 'lengthinmm': 143, 'lengthunitsinferred': 1})

    def test_search_and_normalize_8(self):
        self.assertDictEqual(
            target.search_and_normalize(['143-63-20-17=13']),
            {'haslength': 1, 'lengthinmm': 143, 'lengthunitsinferred': 1})

    def test_search_and_normalize_9(self):
        self.assertDictEqual(
            target.search_and_normalize(['snout-vent length=54 mm; total length=111 mm; tail length=57 mm; weight=5 g']),
            {'haslength': 1, 'lengthinmm': 111, 'lengthunitsinferred': 0})

    def test_search_and_normalize_10(self):
        self.assertDictEqual(
            target.search_and_normalize(['unformatted measurements=Verbatim weight=X;ToL=230;TaL=115;HF=22;E=18;'
                                         ' total length=230 mm; tail length=115 mm;']),
            {'haslength': 1, 'lengthinmm': 230, 'lengthunitsinferred': 0})

    def test_search_and_normalize_11(self):
        self.assertDictEqual(
            target.search_and_normalize(['** Body length =345 cm; Blubber=1 cm ']),
            {'haslength': 1, 'lengthinmm': 3450, 'lengthunitsinferred': 0})

    def test_search_and_normalize_12(self):
        self.assertDictEqual(
            target.search_and_normalize(['t.l.= 2 feet 3.1 - 4.5 inches ']),
            {'haslength': 1, 'lengthinmm': 0, 'lengthunitsinferred': 0})

    def test_search_and_normalize_13(self):
        self.assertDictEqual(
            target.search_and_normalize(['2 ft. 3.1 - 4.5 in. ']),
            {'haslength': 1, 'lengthinmm': 0, 'lengthunitsinferred': 0})

    def test_search_and_normalize_14(self):
        self.assertDictEqual(
            target.search_and_normalize(['total length= 2 ft.']),
            {'haslength': 1, 'lengthinmm': 610, 'lengthunitsinferred': 0})

    def test_search_and_normalize_15(self):
        self.assertDictEqual(
            target.search_and_normalize(['AJR-32   186-102-23-15  15.0g']),
            {'haslength': 1, 'lengthinmm': 186, 'lengthunitsinferred': 1})

    def test_search_and_normalize_16(self):
        self.assertDictEqual(
            target.search_and_normalize(['length=8 mm']),
            {'haslength': 1, 'lengthinmm': 8, 'lengthunitsinferred': 0})

    def test_search_and_normalize_17(self):
        self.assertDictEqual(
            target.search_and_normalize(['another; length=8 mm']),
            {'haslength': 1, 'lengthinmm': 8, 'lengthunitsinferred': 0})

    def test_search_and_normalize_18(self):
        self.assertDictEqual(
            target.search_and_normalize(['another; TL_120, noise']),
            {'haslength': 1, 'lengthinmm': 120, 'lengthunitsinferred': 1})

    def test_search_and_normalize_19(self):
        self.assertDictEqual(
            target.search_and_normalize(['another; TL - 101.3mm, noise']),
            {'haslength': 1, 'lengthinmm': 101.3, 'lengthunitsinferred': 0})

    def test_search_and_normalize_20(self):
        self.assertDictEqual(
            target.search_and_normalize(['before; TL153, after']),
            {'haslength': 1, 'lengthinmm': 153, 'lengthunitsinferred': 1})

    def test_search_and_normalize_21(self):
        self.assertDictEqual(
            target.search_and_normalize(['before; Total length in catalog and specimen tag as 117, after']),
            {'haslength': 1, 'lengthinmm': 117, 'lengthunitsinferred': 1})

    def test_search_and_normalize_22(self):
        self.assertDictEqual(
            target.search_and_normalize(['before Snout vent lengths range from 16 to 23 mm. after']),
            {'haslength': 1, 'lengthinmm': 0, 'lengthunitsinferred': 0})

    def test_search_and_normalize_23(self):
        self.assertDictEqual(
            target.search_and_normalize(['Size=13 cm TL']),
            {'haslength': 1, 'lengthinmm': 130, 'lengthunitsinferred': 0})

    def test_search_and_normalize_24(self):
        self.assertDictEqual(
            target.search_and_normalize(['det_comments:31.5-58.3inTL']),
            {'haslength': 1, 'lengthinmm': 0, 'lengthunitsinferred': 0})

    def test_search_and_normalize_25(self):
        self.assertDictEqual(
            target.search_and_normalize(['SVL52mm']),
            {'haslength': 1, 'lengthinmm': 52, 'lengthunitsinferred': 0})

    def test_search_and_normalize_26(self):
        self.assertDictEqual(
            target.search_and_normalize(['snout-vent length=221 mm; total length=257 mm; tail length=36 mm']),
            {'haslength': 1, 'lengthinmm': 257, 'lengthunitsinferred': 0})

    def test_search_and_normalize_27(self):
        self.assertDictEqual(
            target.search_and_normalize(['SVL 209 mm, total 272 mm, 4.4 g.']),
            {'haslength': 1, 'lengthinmm': 272, 'lengthunitsinferred': 0})

    def test_search_and_normalize_28(self):
        self.assertDictEqual(
            target.search_and_normalize(['{"time collected":"0712-0900", "length":"12.0" }']),
            {'haslength': 1, 'lengthinmm': 12.0, 'lengthunitsinferred': 1})

    def test_search_and_normalize_29(self):
        self.assertDictEqual(
            target.search_and_normalize('{"time collected":"1030", "water depth":"1-8", "bottom":"abrupt lava '
                                        'cliff dropping off to sand at 45 ft.", "length":"119-137" }'),
            {'haslength': 0, 'lengthinmm': None, 'lengthunitsinferred': None})

    def test_search_and_normalize_30(self):
        self.assertDictEqual(
            target.search_and_normalize(['TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx']),
            {'haslength': 1, 'lengthinmm': 44, 'lengthunitsinferred': 0})

    def test_search_and_normalize_31(self):
        self.assertDictEqual(
            target.search_and_normalize(['{"totalLengthInMM":"270-165-18-22-31", ']),
            {'haslength': 1, 'lengthinmm': 270, 'lengthunitsinferred': 0})

    def test_search_and_normalize_32(self):
        self.assertDictEqual(
            target.search_and_normalize(['{"length":"20-29" }']),
            {'haslength': 1, 'lengthinmm': 0, 'lengthunitsinferred': 1})

    def test_search_and_normalize_33(self):
        self.assertDictEqual(
            target.search_and_normalize(['field measurements on fresh dead specimen were 157-60-20-19-21g']),
            {'haslength': 1, 'lengthinmm': 157, 'lengthunitsinferred': 1})

    def test_search_and_normalize_34(self):
        self.assertDictEqual(
            target.search_and_normalize(['f age class: adult; standard length: 63-107mm']),
            {'haslength': 1, 'lengthinmm': 0, 'lengthunitsinferred': 0})

    def test_search_and_normalize_35(self):
        self.assertEqual(
            target.search_and_normalize(['Rehydrated in acetic acid 7/1978-8/1987.']),
            {'lengthinmm': None, 'haslength': 0, 'lengthunitsinferred': None})

    def test_search_and_normalize_36(self):
        self.assertDictEqual(
            target.search_and_normalize(['age class: adult; standard length: 18.0-21.5mm']),
            {'haslength': 1, 'lengthinmm': 0, 'lengthunitsinferred': 0})

    def test_search_and_normalize_37(self):
        self.assertDictEqual(
            target.search_and_normalize(['age class: adult; standard length: 18-21.5mm']),
            {'haslength': 1, 'lengthinmm': 0, 'lengthunitsinferred': 0})

    def test_search_and_normalize_38(self):
        self.assertDictEqual(
            target.search_and_normalize(['age class: adult; standard length: 18.0-21mm']),
            {'haslength': 1, 'lengthinmm': 0, 'lengthunitsinferred': 0})

    def test_search_and_normalize_39(self):
        self.assertDictEqual(
            target.search_and_normalize(['age class: adult; standard length: 18-21mm']),
            {'haslength': 1, 'lengthinmm': 0, 'lengthunitsinferred': 0})

    def test_search_and_normalize_40(self):
        self.assertEqual(
            target.search_and_normalize("Specimen #'s - 5491,5492,5498,5499,5505,5526,5527,5528,5500,"
                                        "5507,5508,5590,5592,5595,5594,5593,5596,5589,5587,5586,5585"),
            {'lengthinmm': None, 'haslength': 0, 'lengthunitsinferred': None})

    def test_search_and_normalize_41(self):
        self.assertEqual(
            target.search_and_normalize(['20-28mm SL']),
            {'haslength': 1, 'lengthinmm': 0, 'lengthunitsinferred': 0})

    def test_search_and_normalize_42(self):
        self.assertEqual(
            target.search_and_normalize(['29mm SL']),
            {'haslength': 1, 'lengthinmm': 29, 'lengthunitsinferred': 0})

    def test_search_and_normalize_43(self):
        self.assertEqual(
            target.search_and_normalize(['{"measurements":"159-?-22-16=21.0" }']),
            {'haslength': 1, 'lengthinmm': 159, 'lengthunitsinferred': 1})

    def test_search_and_normalize_44(self):
        self.assertEqual(
            target.search_and_normalize(['c701563b-dbd9-4500-184f-1ad61eb8da11']),
            {'lengthinmm': None, 'haslength': 0, 'lengthunitsinferred': None})

    def test_search_and_normalize_45(self):
        self.assertEqual(
            target.search_and_normalize(['Meas: L: 21.0']),
            {'haslength': 1, 'lengthinmm': 21.0, 'lengthunitsinferred': 1})

    def test_search_and_normalize_46(self):
        self.assertEqual(
            target.search_and_normalize(['Meas: L: 21.0 cm']),
            {'haslength': 1, 'lengthinmm': 210.0, 'lengthunitsinferred': 0})

    def test_search_and_normalize_47(self):
        self.assertEqual(
            target.search_and_normalize(['LABEL. LENGTH 375 MM.']),
            {'haslength': 1, 'lengthinmm': 375, 'lengthunitsinferred': 0})

    def test_search_and_normalize_48(self):
        self.assertEqual(
            target.search_and_normalize(['SL=12mm']),
            {'haslength': 1, 'lengthinmm': 12, 'lengthunitsinferred': 0})

    def test_search_and_normalize_49(self):
        self.assertEqual(
            target.search_and_normalize(['Size=SL 12-14 mm']),
            {'haslength': 1, 'lengthinmm': 0, 'lengthunitsinferred': 0})

    def test_search_and_normalize_50(self):
        self.assertEqual(
            target.search_and_normalize(['SV 1.2']),
            {'haslength': 1, 'lengthinmm': 1.2, 'lengthunitsinferred': 1})

    def test_search_and_normalize_51(self):
        self.assertEqual(
            target.search_and_normalize([' Length: 123 mm SL']),
            {'haslength': 1, 'lengthinmm': 123, 'lengthunitsinferred': 0})

    def test_search_and_normalize_52(self):
        self.assertEqual(
            target.search_and_normalize([' Length: 12-34 mmSL']),
            {'haslength': 1, 'lengthinmm': 0, 'lengthunitsinferred': 0})

    def test_search_and_normalize_53(self):
        self.assertEqual(
            target.search_and_normalize(['Measurements: L: 21.0 cm']),
            {'haslength': 1, 'lengthinmm': 210.0, 'lengthunitsinferred': 0})

    def test_search_and_normalize_54(self):
        self.assertEqual(
            target.search_and_normalize(['SVL=44']),
            {'haslength': 1, 'lengthinmm': 44, 'lengthunitsinferred': 1})

target = TotalLengthParser()
suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestTotalLengthParser)
unittest.TextTestRunner().run(suite)
