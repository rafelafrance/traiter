"""Find body mass measurements."""

from lib.regexp_list import RegexpList
from lib.trait_parser import TraitParser


class ParseBodyMass(TraitParser):
    """Find body mass measurements."""

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

    common_patterns = TraitParser.common_regex_mass_length + r"""
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

            # Keywords for total mass
            (?P<total_wt_key>
                weightingrams | massingrams
                | (?: body | full | observed | total )
                    (?&dot) \s* (?&wt_key_word)
            )

            # Keywords often used for total mass
            (?P<other_wt_key>
                (?: dead | live ) (?&dot) \s* (?&wt_key_word) )

            #  Weight keyword
            (?P<wt_key_word> weights?
                           | weigh (?: s | ed | ing )
                           | mass
                           | w (?&dot) t s? (?&dot) )

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

            # Mass unit words
            (?P<wt_units_word>
                (?: gram | milligram | kilogram | pound | ounce ) s? )

            # Mass unit abbreviations
            (?P<wt_units_abbrev>
                (?: m (?&dot) g
                | k (?&dot) g
                | g[mr]?
                | lb
                | oz )
                s? (?&dot) )

            # All mass units
            (?P<wt_units> (?&wt_units_word) | (?&wt_units_abbrev) )

            # Use to parse forms like: 2 lbs 4 oz.
            (?P<wt_pound> (?: pound | lb ) s? (?&dot) )
            (?P<wt_ounce> (?: ounce | oz ) s? (?&dot) )
        )"""

    key_conversions = {
        '_english_': 'total weight',
        '_shorthand_': 'total weight',
        'body': 'total weight',
        'body mass': 'total weight',
        'body weight': 'total weight',
        'body wt': 'total weight',
        'body wt.': 'total weight',
        'bodymass': 'total weight',
        'catalog': 'total weight',
        'dead. weight': 'total weight',
        'dead. wt': 'total weight',
        'dead. wt.': 'total weight',
        'full.weight': 'total weight',
        'live weight': 'total weight',
        'live wt': 'total weight',
        'live wt.': 'total weight',
        'mass': 'total weight',
        'massingrams': 'total weight',
        'meas': 'total weight',
        'meas.': 'total weight',
        'measurement': 'total weight',
        'measurements': 'total weight',
        'measurements are': 'total weight',
        'measurements questionable': 'total weight',
        'measurements read': 'total weight',
        'measurements reads': 'total weight',
        'mesurements': 'total weight',
        'observedweight': 'total weight',
        'on tag': 'total weight',
        'specimen': 'total weight',
        'total': 'total weight',
        'total weight': 'total weight',
        'total wt': 'total weight',
        'total wt.': 'total weight',
        'w.t.': 'total weight',
        'weighed': 'total weight',
        'weighing': 'total weight',
        'weighs': 'total weight',
        'weight': 'total weight',
        'weightingrams': 'total weight',
        'weights': 'total weight',
        'wt': 'total weight',
        'wt.': 'total weight',
        'wts': 'total weight',
        'wts.': 'total weight'}

    unit_conversions = {
        '': 1.0,
        '_g_': 1.0,
        'g': 1.0,
        'g.': 1.0,
        'gm': 1.0,
        'gm.': 1.0,
        'gms': 1.0,
        'gms.': 1.0,
        'gr': 1.0,
        'gr.': 1.0,
        'gram': 1.0,
        'grams': 1.0,
        'grs': 1.0,
        'kg': 1000.0,
        'kg.': 1000.0,
        'kgs': 1000.0,
        'kgs.': 1000.0,
        'kilograms': 1000.0,
        'lb': 453.593,
        'lb oz': [453.593, 28.349],
        'lb oz.': [453.593, 28.349],
        'lb ozs': [453.593, 28.349],
        'lb.': 453.593,
        'lb. oz': [453.593, 28.349],
        'lb. oz.': [453.593, 28.349],
        'lb. ozs': [453.593, 28.349],
        'lb. ozs.': [453.593, 28.349],
        'lbs': 453.593,
        'lbs oz': [453.593, 28.349],
        'lbs oz.': [453.593, 28.349],
        'lbs ozs': [453.593, 28.349],
        'lbs.': 453.593,
        'lbs. oz': [453.593, 28.349],
        'lbs. oz.': [453.593, 28.349],
        'lbs. ozs.': [453.593, 28.349],
        'mg': 0.001,
        'mg.': 0.001,
        'mgs.': 0.001,
        'mgs': 0.001,
        'ounce': 28.349,
        'ounces': 28.349,
        'oz': 28.349,
        'oz.': 28.349,
        'ozs': 28.349,
        'ozs.': 28.349,
        'pound': 453.593,
        'pound ounces': [453.593, 28.349],
        'pound oz': [453.593, 28.349],
        'pounds': 453.593,
        'pounds ounces': [453.593, 28.349],
        'pounds ounces.': [453.593, 28.349]}
