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
__version__ = "life_stage_parser.py 2016-08-07T12:53+02:00"

from trait_parsers.parser_battery import ParserBattery
from trait_parsers.trait_parser import TraitParser

class LifeStageParser(TraitParser):

    def __init__(self):
        self.normalize = False
        self.battery = self._battery(self._common_patterns())

    def success(self, result):
        return {'haslifestage': 1, 'derivedlifestage': result['value']}

    def fail(self):
        return {'haslifestage': 0, 'derivedlifestage': ''}

    def _battery(self, common_patterns):
        battery = ParserBattery(exclude_pattern=r''' ^ determin ''')

        # Look for a key and value that is terminated with a delimiter
        battery.append(
            'life_stage_key_value_delimited',
            common_patterns + r'''
                \b (?P<key> (?: life \s* stage (?: \s* remarks )? | age (?: \s* class )? ) )
                \W+
                (?P<value> (?&word_chars) (?: \s+(?&word_chars) ){0,4} ) \s*
                (?: [:;,"] | $ )
            '''
        )

        # Look for a key and value without a clear delimiter
        battery.append(
            'life_stage_key_value_undelimited',
            common_patterns + r'''
                \b (?P<key> life \s* stage (?: \s* remarks )?
                        | age \s* class
                        | age \s* in \s* (?: hour | day ) s?
                        | age
                    )
                    \W+
                    (?P<value> [\w?.\/\-]+ (?: \s+ (?: year | recorded ) )? )
            '''
        )

        # Look for common life stage phrases
        battery.append(
            'life_stage_no_keyword',
            common_patterns + r'''
                (?P<value> (?: after \s+ )?
                        (?: first | second | third | fourth | hatching ) \s+
                        year )
            '''
        )

        battery.append(
            'life_stage_yolk_sac',
            common_patterns + r'''
                (?P<value> (?: yolk ) \s+
                        sac )
            '''
        )

        # Look for the words lifestage words without keys
        # Combinations with embryo and fetus were removed, as more often than not these
        # were reproductiveCondition indicators of and adult female.
        battery.append(
            'life_stage_unkeyed',
            r'''
                \b (?P<value> (?: larves? |larvae? | larvals? | imagos? | neonates? 
                | hatchlings? | hatched? | fry? | metamorphs? | premetamorphs
                | tadpoles? | têtard?
                | young-of-the-year? | leptocephales? | leptocephalus? 
                | immatures? | imms? | jeunes? | young? | ygs?
                | fleglings? | fledgelings? | chicks? | nestlings? 
                | juveniles? | juvéniles? | juvs?
                | subadults? | subadultes? | subads? | sub-adults? | yearlings?
                | matures? | adults? | adulte? | ads? ) (?: \s* \? )? ) \b
            '''
        )

        return battery

    def _common_patterns(self):
        return r'''
            (?(DEFINE)
                (?P<word_chars> [\w?.\/\-]+ )
            )
        '''
