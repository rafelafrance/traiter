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
__copyright__ = "Copyright 2017 vertnet.org"
__version__ = "trait_parser.py 2017-04-27T16:37-04:00"
__kurator_content_type__ = "utility"
__adapted_from__ = ""

import re

class TraitParser:
    IS_RANGE = re.compile(r'- | to', flags=re.IGNORECASE | re.VERBOSE)
    WS_SPLIT = re.compile(r'\s\s\s+')

    def parse_first(self, strings):
        """Look for the first string that parses successfully."""
        for string in strings:
            if string:
                trait = self.parse(string)
                if trait:
                    return trait
        return None

    def parse(self, string):
        """Apply the battery of regular expressions to a string."""
        string = '  '.join(self.WS_SPLIT.split(string.strip()))
#        print 'string: %s\nparse().parsed:\n%s' % (string, self.battery.parse(string))
        return self.battery.parse(string)

    def search(self, strings):
        """Search for a good parse in the strings."""
        parsed = self.parse_first(strings)
        if parsed:
            return self.success(parsed)
        return self.fail()

    def preferred_or_search(self, preferred, strings):
        """If there is a preferred value use it otherwise do a search."""
        preferred = preferred.strip()
        if preferred:
            return self.success({'value': preferred})
        return self.search(strings)

    def search_and_normalize(self, strings):
        """Search for a good parse and normalize the results."""
#        print 'strings: %s' % strings
        joinedstring = ''
        for string in strings:
            if string is not None:
                joinedstring += ';   '+string
#        print 'joinedstring: %s' % joinedstring
        parsed = self.parse(joinedstring)
#        print 'parsed: %s' % parsed
        if parsed is not None:
            normalized = self.normalize(parsed)
#            print 'normalized:\n%s' % normalized
            return self.success(normalized)
        return self.fail()

    def normalize(self, parsed):
        key = None
        if 'key' in parsed and parsed['key']:
            if parsed['key'].lower() in self.key_conversions:
                key = self.key_conversions[parsed['key'].lower()]

        if isinstance(parsed['units'], list):
            units  = ' '.join(parsed['units']).lower()
            if len(self.IS_RANGE.split(parsed['value'][0])) > 1 or \
               len(self.IS_RANGE.split(parsed['value'][1])) > 1:
                return {'value': None, 'is_inferred': 0, 'n_key': key + ' range'}
            else:
                value  = self.multiply(parsed['value'][0], self.unit_conversions[units][0])
                value += self.multiply(parsed['value'][1], self.unit_conversions[units][1])
                return {'value': value, 'is_inferred': 0, 'n_key': key}

        values = self.IS_RANGE.split(parsed['value'])
        if len(values) > 1:
            # If value is a range, do not process
            return {'value': None, 'is_inferred': None, 'n_key': key + ' range'}

        units = parsed.get('units', self.default_units)
        units = units.lower() if units else self.default_units
        is_inferred = int(units[0] == '_' if units else True)

        # Value is just a number and optional units like "3.1 g"
        value = self.multiply(values[0], self.unit_conversions[units])
        
        if value == 0:
            # If value is a zero, do not process
            return {'value': None, 'is_inferred': None, 'n_key': None}

        return {'value': value, 'is_inferred': is_inferred, 'n_key': key}

    def multiply(self, value, units):
        value = re.sub(r'[^\d\.]', '', value)
        precision = 0
        parts = value.split('.')
        if len(parts) > 1:
            precision = len(parts[1])
        result = round(float(value) * units, precision)
#        print 'value: %s units: %s result: %s' % (value, units, result)
        return result if precision else int(result)

    def CommonRegexMassLength(self):
        """Regular expression subexpression used in both length and mass parsing."""
        return r'''
            (?(DEFINE)

                # For our purposes numbers are always positive and decimals.
                (?P<number> (?&open) (?: \d{1,3} (?: , \d{3} ){1,3} | \d+ ) (?: \. \d+ )? (?&close) [\*]? )

                # We also want to pull in number ranges when appropriate.
                (?P<range> (?&number) (?: \s* (?: - | to ) \s* (?&number) )? )

                # Characters that follow a keyword
                (?P<key_end>  \s* [^\w.\[\(]* \s* )

                # We sometimes want to guarantee no word precedes another word.
                # This cannot be done with negative look behind,
                # so we do a positive search for a separator
                (?P<no_word>  (?: ^ | [;,:"'\{\[\(]+ ) \s* )

                # Keywords that may precede a shorthand measurement
                (?P<shorthand_words> on \s* tag
                                | specimens?
                                | catalog
                                | measurements (?: \s+ [\p{Letter}]+)
                                | tag \s+ \d+ \s* =? (?: male | female)? \s* ,
                                | meas [.,]? (?: \s+ \w+ \. \w+ \. )?
                )

                # Common keyword misspellings that precede shorthand measurement
                (?P<shorthand_typos>  mesurements | Measurementsnt )

                # Keys where we need units to know if it's for mass or length
                (?P<key_units_req> measurements? | body | total )

                # Characters that separate shorthand values
                (?P<shorthand_sep> [:\/\-\s] )

                # Used in shorthand notation for unknown values
                (?P<shorthand_unknown> [\?x] )

                # Look for an optional dash or space character
                (?P<dash>     [\s\-]? )
                (?P<dash_req> [\s\-]  )

                # Look for an optional dot character
                (?P<dot> \.? )

                # Numbers are sometimes surrounded by brackets or parentheses
                # Don't worry about matching the opening and closing brackets
                (?P<open>  [\(\[\{]? )
                (?P<close> [\)\]\}]? )
            )
        '''
