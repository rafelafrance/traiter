"""Find total length measurements."""

from lib.regexp_list import RegexpList
from lib.trait_parser import TraitParser
import lib.units as units
import lib.trait_parsers.common_regexp as common_regexp


class ParseTotalLength(TraitParser):
    """Find total length measurements."""

    unit_conversions = units.LENGTH_CONVERSIONS

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
            'found': True,
            'regex': result['regex'],
            'key': result['key'],
            'field': result['field'],
            'start': result['start'],
            'end': result['end'],
            'millimeters': result['value'],
            'units_inferred': result['is_inferred']}

    @staticmethod
    def fail():
        """Return this when the measurement is not found."""
        return {
            'found': False,
            'regex': None,
            'field': None,
            'start': None,
            'end': None,
            'key': None,
            'millimeters': None,
            'units_inferred': False}

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
            'len_key_suffix',
            common_patterns + r"""
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
            'other_len_key',
            common_patterns + r"""
                \b (?P<key>   (?&other_len_key)) (?&key_end)
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&len_units))?
                   """)

        # Look for keys where the units are required
        regexp_list.append(
            'key_units_req',
            common_patterns + r"""
                \b (?P<key>   (?&key_units_req)) (?&key_end)
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&len_units))
                   """)

        # These ambiguous keys have a suffix that disambiguate them
        regexp_list.append(
            'len_key_ambiguous_suffix',
            common_patterns + r"""
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
            'len_key_abbrev',
            common_patterns + r"""
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
            'len_in_phrase',
            common_patterns + r"""
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
            'svl_len_key',
            common_patterns + r"""
                \b (?P<key>   (?&svl_len_key)) (?&key_end)
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&len_units))?""")

        return regexp_list

    common_patterns = common_regexp.SHORT_PATTERNS \
        + common_regexp.LENGTH_PATTERNS \
        + common_regexp.NUMERIC_PATTERNS \
        + r"""
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

        )"""
