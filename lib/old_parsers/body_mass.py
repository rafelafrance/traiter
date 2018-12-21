"""Find body mass measurements."""

from lib.regexp_list import RegexpList
from lib.trait_parser import TraitParser
import lib.units as units
import lib.trait_parsers.common_regexp as common_regexp


class ParseBodyMass(TraitParser):
    """Find body mass measurements."""

    unit_conversions = units.MASS_CONVERSIONS

    def __init__(self, args, preferred_value=None):
        """Add defaults for the measurements."""
        super().__init__()
        self.args = args
        self.regexp_list = self._battery(self.common_patterns)
        self.default_units = '_g_'
        self.preferred_value = preferred_value
        self.parser = self.search_and_normalize

    def success(self, result):
        """Return this when the measurement is found."""
        if result['value'] == 0:
            # Don't allow a 0 mass
            return self.fail()

        return {
            'found': True,
            'regex': result['regex'],
            'field': result['field'],
            'start': result['start'],
            'end': result['end'],
            'key': result['key'],
            'grams': result['value'],
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
            'grams': None,
            'units_inferred': False}

    def _battery(self, common_patterns):
        regexp_list = RegexpList(
            self.args,
            parse_units=True,
            units_from_key=r""" (?P<units> grams ) $ """)

        # Look for a pattern like: body mass: 4 lbs 8 oz
        regexp_list.append(
            'en_wt',
            common_patterns + r"""
                \b (?P<key>    (?&all_wt_keys))? (?&key_end)?
                   (?P<value1> (?&range))    \s*
                   (?P<units1> (?&wt_pound)) \s*
                   (?P<value2> (?&range))    \s*
                   (?P<units2> (?&wt_ounce))
                """,
            default_key='_english_',
            compound_value=2)

        # Look for body mass with a total weight key and optional units
        regexp_list.append(
            'total_wt_key',
            common_patterns + r"""
                \b (?P<key>   (?&total_wt_key)) (?&key_end)
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&wt_units))?
                """)

        # Look for these secondary body mass keys next
        regexp_list.append(
            'other_wt_key',
            common_patterns + r"""
                \b (?P<key>   (?&other_wt_key)) (?&key_end)
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&wt_units))?
                """)

        # Look for keys where the units are required
        regexp_list.append(
            'key_units_req',
            common_patterns + r"""
                \b (?P<key>   (?&key_units_req)) (?&key_end)
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&wt_units))
                """)

        # Look for the body mass in a phrase
        regexp_list.append(
            'wt_in_phrase',
            common_patterns + r"""
                \b (?P<key>   (?&wt_in_phrase)) \D{1,32}
                   (?P<value> (?&range)) \s*
                   (?P<units> (?&wt_units))?
                """)

        # An out of order parse: body mass (g) 20-25
        regexp_list.append(
            'wt_key_word',
            common_patterns + r"""
                \b (?P<key>   (?&wt_key_word)) \s*
                   (?&open) \s* (?P<units> (?&wt_units)) \s* (?&close) \s*
                   (?P<value> (?&range))
                """)

        # These keys require units to disambiguate what is being measured
        regexp_list.append(
            'wt_key_word_req',
            common_patterns + r"""
                (?P<key>   (?&wt_key_word)) (?&key_end)
                (?P<value> (?&range)) \s*
                (?P<units> (?&wt_units))
                """)

        # Body mass is in shorthand notation
        regexp_list.append(
            'wt_shorthand',
            common_patterns + r"""
                \b (?: (?P<key> (?&all_wt_keys)) (?&key_end) )?
                   (?&wt_shorthand) \s*
                   (?P<value> (?&number)) \s*
                   (?P<units> (?&wt_units))?
                """,
            default_key='_shorthand_')

        # Body mass is in shorthand notation (units required)
        regexp_list.append(
            'wt_shorthand_req',
            common_patterns + r"""
                \b (?: (?P<key> (?&all_wt_keys)) (?&key_end) )?
                   (?&wt_shorthand_req) \s*
                   (?P<value> (?&number)) \s*
                   (?P<units> (?&wt_units))
                """,
            default_key='_shorthand_')

        # A shorthand notation with some abbreviations in it
        regexp_list.append(
            'wt_shorthand_euro',
            common_patterns + r"""
                \b (?: (?P<key> (?&all_wt_keys)) (?&key_end) )?
                   (?&wt_shorthand_euro) \s*
                   (?P<value> (?&number)) \s*
                   (?P<units> (?&wt_units))?
                """,
            default_key='_shorthand_')

        # A notation using 'fa'.
        # It can be shorter than the other shorthand notations
        regexp_list.append(
            'wt_fa',
            common_patterns + r"""
                fa \d* -
                (?P<value> (?&number)) \s*
                (?P<units> (?&wt_units))?
                """,
            default_key='_shorthand_')

        # Now we can look for the body mass, RANGE, optional units
        regexp_list.append(
            'wt_key_ambiguous',
            common_patterns + r"""
                (?P<key>   (?&wt_key_word)) (?&key_end)
                (?P<value> (?&range)) \s*
                (?P<units> (?&wt_units))?
                """)

        return regexp_list

    common_patterns = common_regexp.SHORT_PATTERNS \
        + common_regexp.MASS_PATTERNS \
        + common_regexp.NUMERIC_PATTERNS \
        + r"""
        (?(DEFINE)

            # Used to indicate that the next measurement in a shorthand
            # notation is total mass
            (?P<wt_shorthand_sep> [=\s\-]+ )

            # Shorthand notation
            (?P<wt_shorthand>
                (?: (?: (?&number)
                    | (?&shorthand_unknown) ) (?&shorthand_sep) ){3,}
                (?: (?&number)
                    | (?&shorthand_unknown) ) (?&wt_shorthand_sep) )

            # Shorthand notation requiring units
            (?P<wt_shorthand_req>
                (?: (?: (?&number) | (?&shorthand_unknown) )
                (?&shorthand_sep) ){4,} )

            # A common shorthand notation
            (?P<wt_shorthand_euro>
                (?: (?&number) | (?&shorthand_unknown) ) hb
                (?: (?&shorthand_sep) (?: (?<! [\w\-] ) (?&number)
                | (?&shorthand_unknown) )[a-z]* ){4,} = )

            # Keywords often used for total mass
            (?P<other_wt_key>
                (?: dead | live ) (?&dot) \s* (?&wt_key_word) )

            # Gather all weight keys
            (?P<all_wt_keys>
                (?&total_wt_key)
                | (?&other_wt_key)
                | (?&wt_key_word)
                | (?&key_units_req)
                | (?&shorthand_words)
                | (?&shorthand_typos))

            # Look for phrases with the total weight
            (?P<wt_in_phrase> total \s+ (?&wt_key_word) )
        )"""
