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
__version__ = "test_sex_parser.py 2016-07-08T07:51+02:00"

import unittest
from trait_parsers.sex_parser import SexParser


class TestSexParser(unittest.TestCase):

    def test_sex_key_value_delimited_1(self):
        self.assertDictEqual(
            target.parse('weight=81.00 g; sex=female ? ; age=u ad.'),
            {'key': 'sex', 'value': 'female ?'})

    def test_sex_key_value_delimited_2(self):
        self.assertDictEqual(
            target.parse('sex=unknown ; crown-rump length=8 mm'),
            {'key': 'sex', 'value': 'unknown'})

    def test_sex_key_value_undelimited_1(self):
        self.assertDictEqual(
            target.parse('sex=F crown rump length=8 mm'),
            {'key': 'sex', 'value': 'F'})

    def test_sex_unkeyed_1(self):
        self.assertDictEqual(
            target.parse('words male female unknown more words'),
            {'key': None, 'value': ['male', 'female']})

    def test_sex_unkeyed_2(self):
        self.assertEqual(
            target.parse('words male female male more words'),
            None)

    def test_excluded_1(self):
        self.assertEqual(
            target.parse('Respective sex and msmt. in mm'),
            None)

    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################

    def test_preferred_or_search_1(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['weight=81.00 g; sex=female ? ; age=u ad.']),
            {'derivedsex': 'female ?', 'hassex': 1})

    def test_preferred_or_search_2(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['sex=unknown ; crown-rump length=8 mm']),
            {'derivedsex': 'unknown', 'hassex': 1})

    def test_preferred_or_search_3(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['sex=F crown rump length=8 mm']),
            {'derivedsex': 'F', 'hassex': 1})

    def test_preferred_or_search_4(self):
        self.assertDictEqual(
            target.preferred_or_search('', ['words male female unknown more words']),
            {'derivedsex': 'male,female', 'hassex': 1})

    def test_preferred_or_search_5(self):
        self.assertEqual(
            target.preferred_or_search('', ['words male female male more words']),
            {'derivedsex': '', 'hassex': 0})

    def test_preferred_or_search_6(self):
        self.assertEqual(
            target.preferred_or_search('', ['Respective sex and msmt. in mm']),
            {'derivedsex': '', 'hassex': 0})

    def test_preferred_or_search_7(self):
        self.assertEqual(
            target.preferred_or_search('', ['mention male in a phrase']),
            {'derivedsex': 'male', 'hassex': 1})

    def test_preferred_or_search_8(self):
        self.assertEqual(
            target.preferred_or_search('', ['male in a phrase']),
            {'derivedsex': 'male', 'hassex': 1})

    def test_preferred_or_search_9(self):
        self.assertEqual(
            target.preferred_or_search('', ['male or female']),
            {'derivedsex': 'male,female', 'hassex': 1})


target = SexParser()
suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSexParser)
unittest.TextTestRunner().run(suite)
