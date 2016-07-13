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
__version__ = "test_life_stage_parser.py 2016-07-08T10:47+02:00"

import unittest
from trait_parsers.life_stage_parser import LifeStageParser

class TestLifeStageParser(unittest.TestCase):

    def test_life_stage_key_value_delimited_1(self):
        self.assertDictEqual(
            target.parse('sex=unknown ; age class=adult/juvenile'),
            {'key': 'age class', 'value': 'adult/juvenile'})

    def test_life_stage_key_value_delimited_2(self):
        self.assertDictEqual(
            target.parse('weight=81.00 g; sex=female ? ; age=u ad.'),
            {'key': 'age', 'value': 'u ad.'})

    def test_life_stage_key_value_delimited_3(self):
        self.assertDictEqual(
            target.parse('weight=5.2 g; age class=over-winter ; total length=99 mm;'),
            {'key': 'age class', 'value': 'over-winter'})

    def test_life_stage_key_value_undelimited_1(self):
        self.assertDictEqual(
            target.parse('sex=female ? ; age=1st year more than four words here'),
            {'key': 'age', 'value': '1st year'})

    def test_life_stage_no_keyword_1(self):
        self.assertDictEqual(
            target.parse('words after hatching year more words'),
            {'key': None, 'value': 'after hatching year'})

    def test_excluded_1(self):
        self.assertEqual(
            target.parse('age determined by 20-sided die'),
            None)

    def test_life_stage_no_keyword_2(self):
        self.assertDictEqual(
            target.parse('LifeStage Remarks: 5-6 wks'),
            {'key': 'LifeStage Remarks', 'value': '5-6 wks'})

    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################

    def test_preferred_or_search_1(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['sex=unknown ; age class=adult/juvenile']),
            {'derivedlifestage': 'adult/juvenile', 'haslifestage': 1})

    def test_preferred_or_search_2(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['weight=81.00 g; sex=female ? ; age=u ad.']),
            {'derivedlifestage': 'u ad.', 'haslifestage': 1})

    def test_preferred_or_search_3(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['weight=5.2 g; age class=over-winter ; total length=99 mm;']),
            {'derivedlifestage': 'over-winter', 'haslifestage': 1})

    def test_preferred_or_search_4(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['sex=female ? ; age=1st year more than four words here']),
            {'derivedlifestage': '1st year', 'haslifestage': 1})

    def test_preferred_or_search_5(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['words after hatching year more words']),
            {'derivedlifestage': 'after hatching year', 'haslifestage': 1})

    def test_preferred_or_search_6(self):
        self.assertEqual(
            target.preferred_or_search('', ['age determined by 20-sided die']),
            {'derivedlifestage': '', 'haslifestage': 0})

    def test_preferred_or_search_7(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['LifeStage Remarks: 5-6 wks']),
            {'derivedlifestage': '5-6 wks', 'haslifestage': 1})

    def test_preferred_or_search_8(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['mentions juvenile']),
            {'derivedlifestage': 'juvenile', 'haslifestage': 1})

    def test_preferred_or_search_9(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['mentions juveniles in the field']),
            {'derivedlifestage': 'juveniles', 'haslifestage': 1})

    def test_preferred_or_search_10(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['one or more adults']),
            {'derivedlifestage': 'adults', 'haslifestage': 1})

    def test_preferred_or_search_11(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['adults']),
            {'derivedlifestage': 'adults', 'haslifestage': 1})

    def test_preferred_or_search_12(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['adult']),
            {'derivedlifestage': 'adult', 'haslifestage': 1})

    def test_preferred_or_search_13(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['Adulte']),
            {'derivedlifestage': 'Adulte', 'haslifestage': 1})

    def test_preferred_or_search_14(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['AGE IMM']),
            {'derivedlifestage': 'IMM', 'haslifestage': 1})

    def test_preferred_or_search_15(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['subadult']),
            {'derivedlifestage': 'subadult', 'haslifestage': 1})

    def test_preferred_or_search_16(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['subadults']),
            {'derivedlifestage': 'subadults', 'haslifestage': 1})

    def test_preferred_or_search_17(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['subadultery']),
            {'derivedlifestage': '', 'haslifestage': 0})

    def test_preferred_or_search_18(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['in which larvae are found']),
            {'derivedlifestage': 'larvae', 'haslifestage': 1})

    def test_preferred_or_search_19(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['larval']),
            {'derivedlifestage': 'larval', 'haslifestage': 1})

    def test_preferred_or_search_20(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['solitary larva, lonely']),
            {'derivedlifestage': 'larva', 'haslifestage': 1})

    def test_preferred_or_search_21(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['juvénile']),
            {'derivedlifestage': 'juvénile', 'haslifestage': 1})

    def test_preferred_or_search_22(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['Têtard']),
            {'derivedlifestage': 'Têtard', 'haslifestage': 1})

    def test_preferred_or_search_23(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['what if it is a subad.?']),
            {'derivedlifestage': 'subad', 'haslifestage': 1})

    def test_preferred_or_search_24(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['subad is a possibility']),
            {'derivedlifestage': 'subad', 'haslifestage': 1})

    def test_preferred_or_search_25(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['one tadpole']),
            {'derivedlifestage': 'tadpole', 'haslifestage': 1})

    def test_preferred_or_search_26(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['two tadpoles']),
            {'derivedlifestage': 'tadpoles', 'haslifestage': 1})

    def test_preferred_or_search_27(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['an ad.']),
            {'derivedlifestage': 'ad', 'haslifestage': 1})

    def test_preferred_or_search_28(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['what about ad']),
            {'derivedlifestage': 'ad', 'haslifestage': 1})

    def test_preferred_or_search_29(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['ad. is a possibility']),
            {'derivedlifestage': 'ad', 'haslifestage': 1})

    def test_preferred_or_search_30(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['ad is also a possibility']),
            {'derivedlifestage': 'ad', 'haslifestage': 1})

    def test_preferred_or_search_31(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['some embryos']),
            {'derivedlifestage': 'embryos', 'haslifestage': 1})

    def test_preferred_or_search_32(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['an embryo']),
            {'derivedlifestage': 'embryo', 'haslifestage': 1})

    def test_preferred_or_search_33(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['embryonic']),
            {'derivedlifestage': '', 'haslifestage': 0})

    def test_preferred_or_search_34(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['IMM']),
            {'derivedlifestage': 'IMM', 'haslifestage': 1})

    def test_preferred_or_search_35(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['immature']),
            {'derivedlifestage': 'immature', 'haslifestage': 1})

    def test_preferred_or_search_36(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['immatures']),
            {'derivedlifestage': 'immatures', 'haslifestage': 1})

    def test_preferred_or_search_37(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['imm.']),
            {'derivedlifestage': 'imm', 'haslifestage': 1})

    def test_preferred_or_search_38(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['juv.']),
            {'derivedlifestage': 'juv', 'haslifestage': 1})

    def test_preferred_or_search_39(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['one juv to rule them all']),
            {'derivedlifestage': 'juv', 'haslifestage': 1})

    def test_preferred_or_search_40(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['how many juvs does it take?']),
            {'derivedlifestage': 'juvs', 'haslifestage': 1})

    def test_preferred_or_search_41(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['juvs.?']),
            {'derivedlifestage': 'juvs', 'haslifestage': 1})

    def test_preferred_or_search_42(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['juvenile(s)']),
            {'derivedlifestage': 'juvenile', 'haslifestage': 1})

    def test_preferred_or_search_43(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['larva(e)']),
            {'derivedlifestage': 'larva', 'haslifestage': 1})

    def test_preferred_or_search_44(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['young']),
            {'derivedlifestage': 'young', 'haslifestage': 1})

    def test_preferred_or_search_45(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['young adult']),
            {'derivedlifestage': 'young', 'haslifestage': 1})

    def test_preferred_or_search_46(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['adult young']),
            {'derivedlifestage': 'adult', 'haslifestage': 1})

    def test_preferred_or_search_47(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['fetus']),
            {'derivedlifestage': 'fetus', 'haslifestage': 1})

    def test_preferred_or_search_48(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['fetuses']),
            {'derivedlifestage': 'fetuses', 'haslifestage': 1})

    def test_preferred_or_search_49(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['sub-adult']),
            {'derivedlifestage': 'sub-adult', 'haslifestage': 1})

    def test_preferred_or_search_50(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['hatched']),
            {'derivedlifestage': 'hatched', 'haslifestage': 1})

    def test_preferred_or_search_51(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['adult(s) and juvenile(s)']),
            {'derivedlifestage': 'adult', 'haslifestage': 1})

    def test_preferred_or_search_52(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['juvenile(s) and adult(s)']),
            {'derivedlifestage': 'juvenile', 'haslifestage': 1})

    def test_preferred_or_search_53(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['young-of-the-year']),
            {'derivedlifestage': 'young-of-the-year', 'haslifestage': 1})

    def test_preferred_or_search_54(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['YOLK SAC']),
            {'derivedlifestage': 'YOLK SAC', 'haslifestage': 1})

target = LifeStageParser()
suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestLifeStageParser)
unittest.TextTestRunner().run(suite)
