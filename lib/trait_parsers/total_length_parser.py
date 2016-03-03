from trait_parsers.parser_battery import ParserBattery
from trait_parsers.trait_parser import TraitParser


class TotalLengthParser(TraitParser):

    def __init__(self):
        self.normalize = True
        self._battery(self._common_patterns())

    def success(self, value):
        return value

    def fail(self):
        return {'hasLength': 0, 'lengthInMM': 0, 'wereLengthUnitsInferred': 0}

    def _battery(self, common_patterns):
        self.battery = ParserBattery(parse_units=True, units_from_key=r''' (?P<units> mm | millimeters ) $ ''')

        # Look for a pattern like: total length: 4 ft 8 in
        self.battery.append(
            'en_len',
            common_patterns + r'''
                \b (?P<key> (?&all_len_keys))? (?&key_end)?
                   (?P<value1> (?&range))    \s*
                   (?P<units1> (?&len_foot)) \s*
                   (?P<value2> (?&range))    \s*
                   (?P<units2> (?&len_inch))
            ''',
            default_key='_english_',
            compound_value=True
        )

        # Look for total key, number (not a range) and optional units
        # Like: total length = 10.5 mm
        self.battery.append(
            'total_len_key_num',
            common_patterns + r'''
                \b (?P<key> (?&total_len_key)) (?&key_end)
                   (?P<value> (?&number)) (?! [\d\-\.] ) \s*
                   (?P<units> (?&len_units))?
            ''',
            default_units='_mm_'
        )

        # Look for these secondary length keys next but allow a range
        self.battery.append(
            'other_len_key',
            common_patterns + r'''
                \b (?P<key>   (?&other_len_key)) (?&key_end)
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&len_units))?
            '''
        )

        # Look for keys where the units are required
        self.battery.append(
            'key_units_req',
            common_patterns + r'''
                \b (?P<key>   (?&key_units_req)) (?&key_end)
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&len_units))
            '''
        )

        # Look for a length in a phrase
        self.battery.append(
            'len_in_phrase',
            common_patterns + r'''
                \b (?P<key>   (?&len_in_phrase)) \D{1,32}
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&len_units))?
            '''
        )

        # These ambiguous keys have a suffix that disambiguate them
        self.battery.append(
            'len_key_ambiguous_units',
            common_patterns + r'''
                (?&no_word) (?&len_key_ambiguous) (?&key_end)
                (?P<value>  (?&range)) \s*
                (?P<units>  (?&len_units))? \s*
                (?P<key>    (?&len_key_suffix))
            '''
        )

        # These keys require units to disambiguate what is being measured
        self.battery.append(
            'len_key_ambiguous_units',
            common_patterns + r'''
                (?&no_word)
                (?P<key>   (?&len_key_ambiguous)) (?&key_end)
                (?P<value> (?&range)) \s*
                (?P<units> (?&len_units))
            '''
        )

        # An out of order parse: tol (mm) 20-25
        self.battery.append(
            'len_key_abbrev',
            common_patterns + r'''
                \b (?P<key>      (?&len_key_abbrev)) \s*
                   (?&open)  \s* (?P<units> (?&len_units)) \s* (?&close) \s*
                   (?P<value>    (?&range))
            '''
        )

        # This parse puts the key at the end: 20-25 mm TL
        self.battery.append(
            'len_key_suffix',
            common_patterns + r'''
                \b (?P<value> (?&range)) \s*
                   (?P<units> (?&len_units))? \s*
                   (?P<key>   (?&len_key_suffix))
            '''
        )

        # Length is in shorthand notation
        self.battery.append(
            'len_shorthand',
            common_patterns + r'''
                \b (?: (?P<key> (?&all_len_keys)) (?&key_end) )?
                   (?P<value> (?&number))
                   (?&len_shorthand)
            ''',
            default_units='_mm_',
            default_key='_shorthand_'
        )

        # A shorthand notation with some abbreviations in it
        self.battery.append(
            'len_shorthand_euro',
            common_patterns + r'''
                \b (?: (?P<key> (?&all_len_keys)) (?&key_end) )?
                   [a-z]*
                   (?P<value>   (?&number))
                   (?&len_shorthand_euro)
            ''',
            default_units='_mm_',
            default_key='_shorthand_'
        )

        # Now we can look for the total length, RANGE, optional units
        # See 'total_len_key_num' above
        self.battery.append(
            'total_len_key',
            common_patterns + r'''
                \b (?P<key>   (?&total_len_key)) (?&key_end)
                (?P<value> (?&range)) \s*
                (?P<units> (?&len_units))?
            ''',
            default_units='_mm_'
        )

        # We will now allow an ambiguous key if it is not preceded by another word
        self.battery.append(
            'len_key_ambiguous',
            common_patterns + r'''
                (?&no_word)
                (?P<key>   (?&len_key_ambiguous)) (?&key_end)
                (?P<value> (?&range))
            '''
        )

        # Look for snout-vent length keys
        self.battery.append(
            'svl_len_key',
            common_patterns + r'''
                \b (?P<key>   (?&svl_len_key)) (?&key_end)
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&len_units))?
            '''
        )

    def _common_patterns(self):
        return self.CommonRegexMassLength() + r'''
            (?(DEFINE)

                # Look for a shorthand total length. Make sure this isn't a date
                (?P<len_shorthand> (?&dash_req) (?: (?&number) | (?&shorthand_unknown) )
                                   (?: (?&shorthand_sep) (?: (?&number) | (?&shorthand_unknown) ) ){2,}
                )

                # The "European" version of the shorthand length
                (?P<len_shorthand_euro> (?&dash_req) (?: (?&number) | (?&shorthand_unknown) )
                                        (?: (?&shorthand_sep)
                                        (?: (?<! [\w\-] ) (?&number) | (?&shorthand_unknown) )
                                        [\p{Letter}]{0,3} ){2,}
                )

                # Keys that indicate we have a total length
                (?P<total_len_key> total  (?&dash) length (?&dash) in (?&dash) mm
                                 | length (?&dash) in (?&dash) millimeters
                                 | (?: total | max | standard ) (?&dash) lengths?
                                 | meas (?: [a-z]* )? (?&dot) : \s* L
                                 | s (?&dot) l (?&dot)
                                 | label (?&dot) \s* lengths?
                )

                # Snout-vent length is sometimes used as a proxy for total length in some groups
                (?P<svl_len_key> snout (?&dash) vent (?&dash) lengths? (?: (?&dash) in (?&dash) mm )?
                               | s (?&dot) v (?&dot) (:? l (?&dot) )?
                               | snout \s+ vent \s+ lengths?
                )

                # Other keys that may be used as a proxy for total length for some groups
                (?P<other_len_key> head  (?&dash) body (?&dash) length (?&dash) in (?&dash) millimeters
                                 | (?: fork | mean | body ) (?&dash) lengths?
                                 | t [o.]? l (?&dot) _?
                )

                # Ambiguous length keys
                (?P<len_key_ambiguous> lengths? | tag )

                # Abbreviations for total length
                (?P<len_key_abbrev> t (?&dot) o? l (?&dot) | s (?&dot) l (?&dot) )

                # For when the key is a suffix like: 44 mm TL
                (?P<len_key_suffix> (?: in \s* )? (?&len_key_abbrev) )

                # Gather all length key types
                (?P<all_len_keys> (?&total_len_key)
                                | (?&svl_len_key)
                                | (?&other_len_key)
                                | (?&len_key_ambiguous)
                                | (?&key_units_req)
                                | (?&shorthand_words)
                                | (?&shorthand_typos)
                )

                # Length keys found in phrases
                (?P<len_in_phrase> (?: total \s+ length | snout \s+ vent \s+ length | standard \s+ length ) s? )

                # Length unit words
                (?P<len_units_word> (?: meter | millimeter | centimeter | foot | feet | inch e? ) s? )

                # Length unit abbreviations
                (?P<len_units_abbrev> (?: [cm] (?&dot) m | in | ft ) (?&dot) s? )

                # All length units
                (?P<len_units> (?&len_units_word) | (?&len_units_abbrev) )

                # Used for parsing forms like: 2 ft 4 inches
                (?P<len_foot> (?: foot | feet | ft ) s? (?&dot) )
                (?P<len_inch> (?: inch e? | in )     s? (?&dot) )
            )
        '''
