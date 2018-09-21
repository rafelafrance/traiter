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
__version__ = "sex_parser.py 2016-07-08T07:51+02:00"

from trait_parsers.parser_battery import ParserBattery
from trait_parsers.trait_parser import TraitParser


class SexParser(TraitParser):

    def __init__(self):
        self.normalize = False
        self.battery = self._battery()

    def success(self, result):
        value = result['value']
        if isinstance(value, list):
            value = ','.join(value)
        return {'hassex': 1, 'derivedsex': value}

    def fail(self):
        return {'hassex': 0, 'derivedsex': ''}

    def _battery(self):
        battery = ParserBattery(exclude_pattern=r''' ^ (?: and | was | is ) $ ''')

        # Look for a key and value that is terminated with a delimiter
        battery.append(
            'sex_key_value_delimited',
            r'''
                \b (?P<key> sex)
                \W+
                (?P<value> [\w?.]+ (?: \s+ [\w?.]+ ){0,2} )
                \s* (?: [:;,"] | $ )
            '''
        )

        # Look for a key and value without a clear delimiter
        battery.append(
            'sex_key_value_undelimited',
            r'''
                \b (?P<key> sex) \W+ (?P<value> \w+ )
            '''
        )

        # Look for the words 'male' or 'female'
        battery.append(
            'sex_unkeyed',
            r'''
                \b (?P<value> (?: males? | females? ) (?: \s* \? )? ) \b
            ''',
            want_array=2
        )

        return battery
