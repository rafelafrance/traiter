"""Find total length measurements."""

from lib.regexp_list import RegexpList
from lib.trait_parser import TraitParser


class ParseTotalLength(TraitParser):
    """Find total length measurements."""

    def __init__(self, args, preferred_value=None):
        """Add defaults for the measurements."""
        super().__init__()
        self.args = args
        self.regexp_list = self._battery(self.common_patterns)
        self.default_units = '_mm_'
        self.preferred_value = preferred_value
        self.parser = self.search_and_normalize

    def success(self, result):
        """Return this when the measurement is found."""
        if result['value'] == 0:
            # Don't allow a 0 length
            return self.fail()

        return {
            'has_length': True,
            'regex': result['regex'],
            'key': result['key'],
            'field': result['field'],
            'start': result['start'],
            'end': result['end'],
            'length_in_mm': result['value'],
            'length_units_inferred': result['is_inferred']}

    @staticmethod
    def fail():
        """Return this when the measurement is not found."""
        return {
            'has_length': False,
            'regex': None,
            'field': None,
            'start': None,
            'end': None,
            'key': None,
            'length_in_mm': None,
            'length_units_inferred': False}

    def _battery(self, common_patterns):
        regexp_list = RegexpList(
            self.args,
            parse_units=True,
            units_from_key=r""" (?P<units> mm | millimeters ) $ """)

        # Look for a pattern like: total length: 4 ft 8 in
        regexp_list.append(
            'en_len',
            common_patterns + r"""
                \b (?P<key> (?&all_len_keys))? (?&key_end)?
                   (?P<value1> (?&range))    \s*
                   (?P<units1> (?&len_foot)) \s*
                   (?P<value2> (?&range))    \s*
                   (?P<units2> (?&len_inch))
                   """,
            default_key='_english_',
            compound_value=True)

        # Look for a pattern like: total length: 4 ft 8 in
        regexp_list.append(
            'len_fract',
            common_patterns + r"""
                \b (?P<key> (?&all_len_keys))? (?&key_end)?
                   (?P<value1> (\d*))        \s*
                   (?P<value2> (\d+ \/ \d+)) \s*
                   (?P<units> (?&len_units))
                   """,
            default_key='_english_',
            compound_value=True)

        # This parse puts the key at the end: 20-25 mm TL
        regexp_list.append(
            'len_key_suffix', common_patterns + r"""
                \b (?P<value> (?&range)) \s*
                   (?P<units> (?&len_units))? \s*
                   (?P<key>   (?&len_key_suffix))
                   """)

        # Look for total key, number (not a range) and optional units
        # Like: total length = 10.5 mm
        regexp_list.append(
            'total_len_key_num',
            common_patterns + r"""
                \b (?P<key> (?&total_len_key)) (?&key_end)
                   (?P<value> (?&number)) (?! \s* [\d\-\.] ) \s*
                   (?P<units> (?&len_units))?
                   """,
            default_units='_mm_')

        # Look for these secondary length keys next but allow a range
        regexp_list.append(
            'other_len_key', common_patterns + r"""
                \b (?P<key>   (?&other_len_key)) (?&key_end)
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&len_units))?
                   """)

        # Look for keys where the units are required
        regexp_list.append(
            'key_units_req', common_patterns + r"""
                \b (?P<key>   (?&key_units_req)) (?&key_end)
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&len_units))
                   """)

        # These ambiguous keys have a suffix that disambiguate them
        regexp_list.append(
            'len_key_ambiguous_suffix', common_patterns + r"""
                (?&no_word) (?&len_key_ambiguous) (?&key_end)
                (?P<value>  (?&range)) \s*
                (?P<units>  (?&len_units))? \s*
                (?P<key>    (?&len_key_suffix))
                """)

        # These keys require units to disambiguate what is being measured
        regexp_list.append(
            'len_key_ambiguous_units', common_patterns + r"""
                (?&no_word)
                (?P<key>   (?&len_key_ambiguous)) (?&key_end)
                (?P<value> (?&range)) \s*
                (?P<units> (?&len_units))
                """)

        # An out of order parse: tol (mm) 20-25
        regexp_list.append(
            'len_key_abbrev', common_patterns + r"""
                \b (?P<key>      (?&len_key_abbrev)) \s*
                   (?&open)  \s* (?P<units> (?&len_units)) \s* (?&close) \s*
                   (?P<value>    (?&range))""")

        # Length is in shorthand notation
        regexp_list.append(
            'len_shorthand',
            common_patterns + r"""
                \b (?: (?P<key> (?&all_len_keys)) (?&key_end) )?
                   (?P<value> (?&number))
                   (?&len_shorthand)
                   """,
            default_units='_mm_',
            default_key='_shorthand_')

        # A shorthand notation with some abbreviations in it
        regexp_list.append(
            'len_shorthand_euro',
            common_patterns + r"""
                \b (?: (?P<key> (?&all_len_keys)) (?&key_end) )?
                   [a-z]*
                   (?P<value>   (?&number))
                   (?&len_shorthand_euro)""",
            default_units='_mm_',
            default_key='_shorthand_')

        # Now we can look for the total length, RANGE, optional units
        # See 'total_len_key_num' above
        regexp_list.append(
            'total_len_key',
            common_patterns + r"""
                \b (?P<key>   (?&total_len_key)) (?&key_end) \s*
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&len_units))?
                """,
            default_units='_mm_')

        # Look for a length in a phrase
        regexp_list.append(
            'len_in_phrase', common_patterns + r"""
                \b (?P<key>   (?&len_in_phrase)) [^\d;]{1,32}
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&len_units))?
                   """)

        #  Now allow an ambiguous key if it is not preceded by another word
        regexp_list.append(
            'len_key_ambiguous', common_patterns + r"""
                (?&no_word)
                (?P<key>   (?&len_key_ambiguous)) (?&key_end)
                (?P<value> (?&range))
                """)

        # Look for snout-vent length keys
        regexp_list.append(
            'svl_len_key', common_patterns + r"""
                \b (?P<key>   (?&svl_len_key)) (?&key_end)
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&len_units))?""")

        return regexp_list

    common_patterns = TraitParser.common_regex_mass_length + r"""
        (?(DEFINE)

            # How numbers are represented in shorthand notation
            (?P<shorthand_num>
                (?: (?&number) | (?&shorthand_unknown) ) )

            # Look for a shorthand total length. Make sure it isn't a date
            (?P<len_shorthand>
                (?&dash_req) (?&shorthand_num)
                (?: (?&shorthand_sep) (?&shorthand_num) ){2,} )

            # The "European" version of the shorthand length
            (?P<len_shorthand_euro>
                (?&dash_req) (?&shorthand_num)
                (?: (?&shorthand_sep)
                (?: (?<! [\w\-] ) (?&shorthand_num) )
                [\p{Letter}]{0,3} ){2,})

            # Keys that indicate we have a total length
            (?P<total_len_key>
                total  (?&dash) length (?&dash) in (?&dash) mm
                | total  (?&dash) length (?&dash) in
                | length (?&dash) in (?&dash) millimeters
                | (?: total | max | standard ) (?&dash) lengths?
                | (?: meas (?: [a-z]* )? (?&dot) : \s* L )
                | s (?&dot) l (?&dot)
                | label (?&dot) \s* lengths?)

            # Snout-vent length is a proxy for total length
            (?P<svl_len_key>
                snout (?&dash) vent
                    (?&dash) lengths? (?: (?&dash) in (?&dash) mm )?
                | s (?&dot) v (?&dot) ( l (?&dot) )?
                | snout \s+ vent \s+ lengths?
            )

            # Other keys that may be used as a total length proxy
            (?P<other_len_key>
                head  (?&dash) body (?&dash)
                    length (?&dash) in (?&dash) millimeters
                | (?: fork | mean | body ) (?&dash) lengths?
                | Meas \s* : \s* Length \s* \(L\)
                | t [o.]? l (?&dot) _?
            )

            # Ambiguous length keys
            (?P<len_key_ambiguous> lengths? | tag )

            # Abbreviations for total length
            (?P<len_key_abbrev>
                t (?&dot) o? l (?&dot) | s (?&dot) l (?&dot) )

            # For when the key is a suffix like: 44 mm TL
            (?P<len_key_suffix> (?: in \s* )? (?&len_key_abbrev) )

            # Gather all length key types
            (?P<all_len_keys>
                (?&total_len_key)
                | (?&svl_len_key)
                | (?&other_len_key)
                | (?&len_key_ambiguous)
                | (?&key_units_req)
                | (?&shorthand_words)
                | (?&shorthand_typos))

            # Length keys found in phrases
            (?P<len_in_phrase>
                (?: total \s+ length
              | snout \s+ vent \s+ length
              | standard \s+ length ) s? )

            # Length unit words
            (?P<len_units_word>
                (?: meter
                | millimeter
                | centimeter
                | foot
                | feet
                | inch e? ) s? )

            # Length unit abbreviations
            (?P<len_units_abbrev>
                (?: [cm] (?&dot) m | in | ft ) (?&dot) s? )

            # All length units
            (?P<len_units> (?&len_units_word) | (?&len_units_abbrev) )

            # Used for parsing forms like: 2 ft 4 inches
            (?P<len_foot> (?: foot | feet | ft ) s? (?&dot) )
            (?P<len_inch> (?: inch e? | in )     s? (?&dot) ))
            """

    key_conversions = {
        '_english_': 'total length',
        '_shorthand_': 'total length',
        'body': 'head-body length',
        'body length': 'head-body length',
        'catalog': 'total length',
        'fork length': 'fork length',
        'forklength': 'fork length',
        'headbodylengthinmillimeters': 'head-body length',
        'label length': 'total length',
        'label. length': 'total length',
        'label.length': 'total length',
        'length': 'total length',
        'lengthinmillimeters': 'total length',
        'lengths': 'total length',
        'max length': 'total length',
        'maxlength': 'total length',
        'mean length': 'total length',
        'meas': 'total length',
        'meas,': 'total length',
        'meas.': 'total length',
        'meas. h.b.': 'head-body length',
        'meas: l': 'total length',
        'measurement': 'total length',
        'measurements': 'total length',
        'measurements are': 'total length',
        'measurements made': 'total length',
        'measurements of': 'total length',
        'measurements questionable': 'total length',
        'measurements read': 'total length',
        'measurements reads': 'total length',
        'measurements: l': 'total length',
        'measurementsnt': 'total length',
        'mesurements': 'total length',
        'on tag': 'total length',
        's.l': 'standard length',
        's.l.': 'standard length',
        's.v.': 'snout-vent length',
        'sl': 'standard length',
        'sl.': 'standard length',
        'snout vent length': 'snout-vent length',
        'snout vent lengths': 'snout-vent length',
        'snout-vent length': 'snout-vent length',
        'snout-vent lengths': 'snout-vent length',
        'snoutventlengthinmm': 'snout-vent length',
        'specimen': 'total length',
        'specimens': 'total length',
        'standard length': 'standard length',
        'sv': 'snout-vent length',
        'svl': 'snout-vent length',
        'svl.': 'snout-vent length',
        't.l': 'total length',
        't.l.': 'total length',
        'tag': 'total length',
        'tl': 'total length',
        'tl.': 'total length',
        'tl_': 'total length',
        'tol': 'total length',
        'total': 'total length',
        'total  length': 'total length',
        'total length': 'total length',
        'total length in mm': 'total length',
        'total lengths': 'total length',
        'totallength': 'total length',
        'totallengthin': 'total length',
        'totallengthinmm': 'total length'}

    unit_conversions = {
        '': 1.0,
        '_mm_': 1.0,
        'c.m.': 10.0,
        'centimeters': 10.0,
        'cm': 10.0,
        'cm.': 10.0,
        'cm.s': 10.0,
        'cms': 10.0,
        'feet': 304.8,
        'feet inch': [304.8, 25.4],
        'feet inches': [304.8, 25.4],
        'feet inches.': [304.8, 25.4],
        'foot': 304.8,
        'foot inch': [304.8, 25.4],
        'foot inches': [304.8, 25.4],
        'foot inches.': [304.8, 25.4],
        'ft': 304.8,
        'ft in': [304.8, 25.4],
        'ft in.': [304.8, 25.4],
        'ft inches': [304.8, 25.4],
        'ft inch': [304.8, 25.4],
        'ft inches.': [304.8, 25.4],
        'ft ins.': [304.8, 25.4],
        'ft.': 304.8,
        'ft. in': [304.8, 25.4],
        'ft. in.': [304.8, 25.4],
        'ft. inches': [304.8, 25.4],
        'ft. ins': [304.8, 25.4],
        'in': 25.4,
        'in.': 25.4,
        'inch': 25.4,
        'inches': 25.4,
        'ins': 25.4,
        'm.m': 1.0,
        'm.m.': 1.0,
        'meter': 1000.0,
        'meters': 1000.0,
        'millimeter': 1.0,
        'millimeters': 1.0,
        'mm': 1.0,
        'mm.': 1.0,
        'mm.s': 1.0,
        'mms': 1.0}
