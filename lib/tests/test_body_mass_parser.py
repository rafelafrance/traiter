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
__version__ = "test_body_mass_parser.py 2016-08-07T14:10+02:00"

import unittest
from trait_parsers.body_mass_parser import BodyMassParser


class TestBodyMassParser(unittest.TestCase):

    def test_1(self):
        self.assertDictEqual(
            target.parse('762-292-121-76 2435.0g'),
            {'key': '_shorthand_', 'value': '2435.0', 'units': 'g'})

    def test_2(self):
        self.assertDictEqual(
            target.parse('TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx'),
            {'key': 'Weight', 'value': '0.77', 'units': 'g'})

    def test_3(self):
        self.assertDictEqual(
            target.parse('Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-62g'),
            {'key': '_shorthand_', 'value': '62', 'units': 'g'})

    def test_4(self):
        self.assertDictEqual(
            target.parse('body mass=20 g'),
            {'key': 'body mass', 'value': '20', 'units': 'g'})

    def test_5(self):
        self.assertDictEqual(
            target.parse('2 lbs. 3.1 - 4.5 oz '),
            {'key': '_english_', 'value': ['2', '3.1 - 4.5'], 'units': ['lbs.', 'oz']})

    def test_6(self):
        self.assertDictEqual(
            target.parse('{"totalLengthInMM":"x", "earLengthInMM":"20", "weight":"[139.5] g" }'),
            {'key': 'weight', 'value': '[139.5]', 'units': 'g'})

    def test_7(self):
        self.assertDictEqual(
            target.parse('{"fat":"No fat", "gonads":"Testes 10 x 6 mm.", "molt":"No molt",'
                         ' "stomach contents":"Not recorded", "weight":"94 gr."'),
            {'key': 'weight', 'value': '94', 'units': 'gr.'})

    def test_8(self):
        self.assertDictEqual(
            target.parse('Note in catalog: 83-0-17-23-fa64-35g'),
            {'key': '_shorthand_', 'value': '35', 'units': 'g'})

    def test_9(self):
        self.assertDictEqual(
            target.parse('{"measurements":"20.2g, SVL 89.13mm" }'),
            {'key': 'measurements', 'value': '20.2', 'units': 'g'})

    def test_10(self):
        self.assertDictEqual(
            target.parse('Body: 15 g'),
            {'key': 'Body', 'value': '15', 'units': 'g'})

    def test_11(self):
        self.assertDictEqual(
            target.parse('82-00-15-21-tr7-fa63-41g'),
            {'key': '_shorthand_', 'value': '41', 'units': 'g'})

    def test_12(self):
        self.assertDictEqual(
            target.parse('weight=5.4 g; unformatted measurements=77-30-7-12=5.4'),
            {'key': 'weight', 'value': '5.4', 'units': 'g'})

    def test_13(self):
        self.assertDictEqual(
            target.parse('unformatted measurements=77-30-7-12=5.4; weight=5.4;'),
            {'key': 'measurements', 'value': '5.4', 'units': None})

    def test_14(self):
        self.assertDictEqual(
            target.parse('{"totalLengthInMM":"270-165-18-22-31", '),
            {'key': '_shorthand_', 'value': '31', 'units': None})

    def test_15(self):
        self.assertDictEqual(
            target.parse('{"measurements":"143-63-20-17=13 g" }'),
            {'key': 'measurements', 'value': '13', 'units': 'g'})

    def test_16(self):
        self.assertDictEqual(
            target.parse('143-63-20-17=13'),
            {'key': '_shorthand_', 'value': '13', 'units': None})

    def test_17(self):
        self.assertDictEqual(
            target.parse('reproductive data: Testes descended -10x7 mm; sex: male;'
                         ' unformatted measurements: 181-75-21-18=22 g'),
            {'key': 'measurements', 'value': '22', 'units': 'g'})

    def test_18(self):
        self.assertDictEqual(
            target.parse('{ "massingrams"="20.1" }'),
            {'key': 'massingrams', 'value': '20.1', 'units': 'grams'})

    def test_19(self):
        self.assertDictEqual(
            target.parse(' {"gonadLengthInMM_1":"10", "gonadLengthInMM_2":"6", "weight":"1,192.0" }'),
            {'key': 'weight', 'value': '1,192.0', 'units': None})

    def test_20(self):
        self.assertDictEqual(
            target.parse('"weight: 20.5-31.8'),
            {'key': 'weight', 'value': '20.5-31.8', 'units': None})

    def test_21(self):
        self.assertDictEqual(
            target.parse('"weight: 20.5-32'),
            {'key': 'weight', 'value': '20.5-32', 'units': None})

    def test_22(self):
        self.assertDictEqual(
            target.parse('"weight: 21-31.8'),
            {'key': 'weight', 'value': '21-31.8', 'units': None})

    def test_23(self):
        self.assertDictEqual(
            target.parse('"weight: 21-32'),
            {'key': 'weight', 'value': '21-32', 'units': None})

    def test_24(self):
        self.assertEqual(
            target.parse("Specimen #'s - 5491,5492,5498,5499,5505,5526,5527,5528,5500,5507,5508,5590,"
                         "5592,5595,5594,5593,5596,5589,5587,5586,5585"),
            None)

    def test_25(self):
        self.assertDictEqual(
            target.parse('weight=5.4 g; unformatted measurements=77-x-7-12=5.4'),
            {'key': 'weight', 'value': '5.4', 'units': 'g'})

    def test_26(self):
        self.assertEqual(
            target.parse('c701563b-dbd9-4500-184f-1ad61eb8da11'),
            None)

    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################

    def test_1(self):
        self.assertDictEqual(
            target.search_and_normalize(['762-292-121-76 2435.0g']),
            {'hasmass': 1, 'massing': 2435.0, 'massunitsinferred': 0})

    def test_2(self):
        self.assertDictEqual(
            target.search_and_normalize(['TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx']),
            {'hasmass': 1, 'massing': 0.77, 'massunitsinferred': 0})

    def test_3(self):
        self.assertDictEqual(
            target.search_and_normalize(['Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-62g']),
            {'hasmass': 1, 'massing': 62, 'massunitsinferred': 0})

    def test_4(self):
        self.assertDictEqual(
            target.search_and_normalize(['body mass=20 g']),
            {'hasmass': 1, 'massing': 20, 'massunitsinferred': 0})

    def test_5(self):
        self.assertDictEqual(
            target.search_and_normalize(['2 lbs. 3.1 - 4.5 oz ']),
            {'hasmass': 0, 'massing': None, 'massunitsinferred': None})

    def test_6(self):
        self.assertDictEqual(
            target.search_and_normalize(['{"totalLengthInMM":"x", "earLengthInMM":"20", "weight":"[139.5] g" }']),
            {'hasmass': 1, 'massing': 139.5, 'massunitsinferred': 0})

    def test_7(self):
        self.assertDictEqual(
            target.search_and_normalize(['{"fat":"No fat", "gonads":"Testes 10 x 6 mm.", "molt":"No molt",'
                                         ' "stomach contents":"Not recorded", "weight":"94 gr."']),
            {'hasmass': 1, 'massing': 94, 'massunitsinferred': 0})

    def test_8(self):
        self.assertDictEqual(
            target.search_and_normalize(['Note in catalog: 83-0-17-23-fa64-35g']),
            {'hasmass': 1, 'massing': 35, 'massunitsinferred': 0})

    def test_9(self):
        self.assertDictEqual(
            target.search_and_normalize(['{"measurements":"20.2g, SVL 89.13mm" }']),
            {'hasmass': 1, 'massing': 20.2, 'massunitsinferred': 0})

    def test_10(self):
        self.assertDictEqual(
            target.search_and_normalize(['Body: 15 g']),
            {'hasmass': 1, 'massing': 15, 'massunitsinferred': 0})

    def test_11(self):
        self.assertDictEqual(
            target.search_and_normalize(['82-00-15-21-tr7-fa63-41g']),
            {'hasmass': 1, 'massing': 41, 'massunitsinferred': 0})

    def test_12(self):
        self.assertDictEqual(
            target.search_and_normalize(['weight=5.4 g; unformatted measurements=77-30-7-12=5.4']),
            {'hasmass': 1, 'massing': 5.4, 'massunitsinferred': 0})

    def test_13(self):
        self.assertDictEqual(
            target.search_and_normalize(['unformatted measurements=77-30-7-12=5.4; weight=5.4;']),
            {'hasmass': 1, 'massing': 5.4, 'massunitsinferred': 1})

    def test_14(self):
        self.assertDictEqual(
            target.search_and_normalize(['{"totalLengthInMM":"270-165-18-22-31", ']),
            {'hasmass': 1, 'massing': 31, 'massunitsinferred': 1})

    def test_15(self):
        self.assertDictEqual(
            target.search_and_normalize(['{"measurements":"143-63-20-17=13 g" }']),
            {'hasmass': 1, 'massing': 13, 'massunitsinferred': 0})

    def test_16(self):
        self.assertDictEqual(
            target.search_and_normalize(['143-63-20-17=13']),
            {'hasmass': 1, 'massing': 13, 'massunitsinferred': 1})

    def test_17(self):
        self.assertDictEqual(
            target.search_and_normalize(['reproductive data: Testes descended -10x7 mm; sex: male;'
                                         ' unformatted measurements: 181-75-21-18=22 g']),
            {'hasmass': 1, 'massing': 22, 'massunitsinferred': 0})

    def test_18(self):
        self.assertDictEqual(
            target.search_and_normalize(['{ "massingrams"="20.1" }']),
            {'hasmass': 1, 'massing': 20.1, 'massunitsinferred': 0})

    def test_19(self):
        self.assertDictEqual(
            target.search_and_normalize([' {"gonadLengthInMM_1":"10", "gonadLengthInMM_2":"6", "weight":"1,192.0" }']),
            {'hasmass': 1, 'massing': 1192.0, 'massunitsinferred': 1})

    def test_20(self):
        self.assertDictEqual(
            target.search_and_normalize(['"weight: 20.5-31.8']),
            {'hasmass': 0, 'massing': None, 'massunitsinferred': None})

    def test_21(self):
        self.assertDictEqual(
            target.search_and_normalize(['"weight: 20.5-32']),
            {'hasmass': 0, 'massing': None, 'massunitsinferred': None})

    def test_22(self):
        self.assertDictEqual(
            target.search_and_normalize(['"weight: 21-31.8']),
            {'hasmass': 0, 'massing': None, 'massunitsinferred': None})

    def test_23(self):
        self.assertDictEqual(
            target.search_and_normalize(['"weight: 21-32']),
            {'hasmass': 0, 'massing': None, 'massunitsinferred': None})

    def test_24(self):
        self.assertEqual(
            target.search_and_normalize(["Specimen #'s - 5491,5492,5498,5499,5505,5526,5527,5528,5500,5507,5508,5590,"
                                         "5592,5595,5594,5593,5596,5589,5587,5586,5585"]),
            {'hasmass': 0, 'massing': None, 'massunitsinferred': None})

    def test_25(self):
        self.assertDictEqual(
            target.search_and_normalize(['weight=5.4 g; unformatted measurements=77-x-7-12=5.4']),
            {'hasmass': 1, 'massing': 5.4, 'massunitsinferred': 0})

    def test_26(self):
        self.assertEqual(
            target.search_and_normalize(['c701563b-dbd9-4500-184f-1ad61eb8da11']),
            {'hasmass': 0, 'massing': None, 'massunitsinferred': None})

    def test_27(self):
        self.assertDictEqual(
            target.search_and_normalize(['body mass=0 g']),
            {'hasmass': 0, 'massing': None, 'massunitsinferred': None})

target = BodyMassParser()
suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestBodyMassParser)
unittest.TextTestRunner().run(suite)
