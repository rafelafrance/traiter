from trait_parsers.parser_battery import ParserBattery
from trait_parsers.trait_parser import TraitParser


class BodyMassParser(TraitParser):

    def __init__(self):
        self.normalize = True
        self._battery(self._common_patterns())

    def success(self, value):
        return value

    def fail(self):
        return {'hasMass': 0, 'massInG': 0, 'wereMassUnitsInferred': 0}

    def _battery(self, common_patterns):
        self.battery = ParserBattery(parse_units=True, units_from_key=r''' (?P<units> grams ) $ ''')

        # Look for a pattern like: body mass: 4 lbs 8 oz
        self.battery.append(
            'en_wt',
            common_patterns + r'''
                \b (?P<key>    (?&all_wt_keys))? (?&key_end)?
                   (?P<value1> (?&range))    \s*
                   (?P<units1> (?&wt_pound)) \s*
                   (?P<value2> (?&range))    \s*
                   (?P<units2> (?&wt_ounce))
            ''',
            default_key='_english_',
            compound_value=2
        )

        # Look for body mass with a total weight key and optional units
        self.battery.append(
            'total_wt_key',
            common_patterns + r'''
                \b (?P<key>   (?&total_wt_key)) (?&key_end)
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&wt_units))?
            '''
        )

        # Look for these secondary body mass keys next
        self.battery.append(
            'other_wt_key',
            common_patterns + r'''
                \b (?P<key>   (?&other_wt_key)) (?&key_end)
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&wt_units))?
            '''
        )

        # Look for keys where the units are required
        self.battery.append(
            'key_units_req',
            common_patterns + r'''
                \b (?P<key>   (?&key_units_req)) (?&key_end)
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&wt_units))
            '''
        )

        # Look for the body mass in a phrase
        self.battery.append(
            'wt_in_phrase',
            common_patterns + r'''
                \b (?P<key>   (?&wt_in_phrase)) \D{1,32}
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&wt_units))?
            '''
        )

        # An out of order parse: body mass (g) 20-25
        self.battery.append(
            'wt_key_word',
            common_patterns + r'''
                \b (?P<key>   (?&wt_key_word)) \s*
                   (?&open) \s* (?P<units> (?&wt_units)) \s* (?&close) \s*
                   (?P<value> (?&range))
            '''
        )

        # These keys require units to disambiguate what is being measured
        self.battery.append(
            'wt_key_word_req',
            common_patterns + r'''
                (?P<key>   (?&wt_key_word)) (?&key_end)
                (?P<value> (?&range)) \s*
                (?P<units> (?&wt_units))
            '''
        )

        # Body mass is in shorthand notation
        self.battery.append(
            'wt_shorthand',
            common_patterns + r'''
                \b (?: (?P<key> (?&all_wt_keys)) (?&key_end) )?
                   (?&wt_shorthand) \s*
                   (?P<value> (?&number)) \s*
                   (?P<units> (?&wt_units))?
            ''',
            default_key='_shorthand_'
        )

        # Body mass is in shorthand notation (units required)
        self.battery.append(
            'wt_shorthand_req',
            common_patterns + r'''
                \b (?: (?P<key> (?&all_wt_keys)) (?&key_end) )?
                   (?&wt_shorthand_req) \s*
                   (?P<value> (?&number)) \s*
                   (?P<units> (?&wt_units))
            ''',
            default_key='_shorthand_'
        )

        # A shorthand notation with some abbreviations in it
        self.battery.append(
            'wt_shorthand_euro',
            common_patterns + r'''
                \b (?: (?P<key> (?&all_wt_keys)) (?&key_end) )?
                   (?&wt_shorthand_euro) \s*
                   (?P<value> (?&number)) \s*
                   (?P<units> (?&wt_units))?
            ''',
            default_key='_shorthand_'
        )

        # A notation using 'fa'. It can be shorter than the other shorthand notations
        self.battery.append(
            'wt_fa',
            common_patterns + r'''
                fa \d* -
                (?P<value> (?&number)) \s*
                (?P<units> (?&wt_units))?
            ''',
            default_key='_shorthand_'
        )

        # Now we can look for the body mass, RANGE, optional units
        self.battery.append(
            'wt_key_ambiguous',
            common_patterns + r'''
                (?P<key>   (?&wt_key_word)) (?&key_end)
                (?P<value> (?&range)) \s*
                (?P<units> (?&wt_units))?
            '''
        )

    def _common_patterns(self):
        return self.CommonRegexMassLength() + r'''
            (?(DEFINE)

                # Used to indicate that the next measurement in a shorthand notation is total mass
                (?P<wt_shorthand_sep> [=\s\-]+ )

                # Shorthand notation
                (?P<wt_shorthand> (?: (?: (?&number) | (?&shorthand_unknown) ) (?&shorthand_sep) ){3,}
                                  (?: (?&number) | (?&shorthand_unknown) ) (?&wt_shorthand_sep) )

                # Shorthand notation requiring units
                (?P<wt_shorthand_req> (?: (?: (?&number) | (?&shorthand_unknown) ) (?&shorthand_sep) ){4,} )

                # A common shorthand notation
                (?P<wt_shorthand_euro> (?: (?&number) | (?&shorthand_unknown) ) hb
                                       (?: (?&shorthand_sep) (?: (?<! [\w\-] ) (?&number)
                                     | (?&shorthand_unknown) )[a-z]* ){4,} = )

                # Keywords for total mass
                (?P<total_wt_key> weightingrams | massingrams
                                | (?: body | full | observed | total ) (?&dot) \s* (?&wt_key_word)
                )

                # Keywords often used for total mass
                (?P<other_wt_key> (?: dead | live ) (?&dot) \s* (?&wt_key_word) )

                #  Weight keyword
                (?P<wt_key_word> weights?
                               | weigh (?: s | ed | ing )
                               | mass
                               | w (?&dot) t s? (?&dot)
                )

                # Gather all weight keys
                (?P<all_wt_keys> (?&total_wt_key)  | (?&other_wt_key) | (?&wt_key_word)
                               | (?&key_units_req) | (?&shorthand_words) | (?&shorthand_typos))

                # Look for phrases with the total weight
                (?P<wt_in_phrase> total \s+ (?&wt_key_word) )

                # Mass unit words
                (?P<wt_units_word> (?: gram | milligram | kilogram | pound | ounce ) s? )

                # Mass unit abbreviations
                (?P<wt_units_abbrev> (?: m (?&dot) g | k (?&dot) g | g[mr]? | lb | oz ) s? (?&dot) )

                # All mass units
                (?P<wt_units> (?&wt_units_word) | (?&wt_units_abbrev) )

                # Use to parse forms like: 2 lbs 4 oz.
                (?P<wt_pound> (?: pound | lb ) s? (?&dot) )
                (?P<wt_ounce> (?: ounce | oz ) s? (?&dot) )
            )
        '''
