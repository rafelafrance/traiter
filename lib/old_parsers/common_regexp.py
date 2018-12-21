"""Holds regular expressions common to more than one parser."""

import regex


IS_RANGE = regex.compile(r'- | to', flags=regex.IGNORECASE | regex.VERBOSE)
IS_FRACT = regex.compile(r'\/', flags=regex.IGNORECASE | regex.VERBOSE)
WS_SPLIT = regex.compile(r'\s\s\s+')
IS_CROSS = regex.compile(
    r'x | by | \*', flags=regex.IGNORECASE | regex.VERBOSE)

SHORT_PATTERNS = r"""
    (?(DEFINE)

        # Characters that follow a keyword
        (?P<key_end>  \s* [^ \w . \[ ( ]* \s* )

        # We sometimes want to guarantee no word precedes another word.
        # This cannot be done with negative look behind,
        # so we do a positive search for a separator
        (?P<no_word>  (?: ^ | [;,:"'\{\[\(]+ ) \s* )

        # Look for an optional dash or space character
        (?P<dash>     [\s\-]? )
        (?P<dash_req> [\s\-]  )

        # Look for an optional dot character
        (?P<dot> \.? )

        # Look for an optional comma character
        (?P<comma> ,? )

        # Numbers are sometimes surrounded by brackets or parentheses
        # Don't worry about matching the opening and closing brackets
        (?P<open>  [\(\[\{]? )
        (?P<close> [\)\]\}]? )

    )"""

NUMERIC_PATTERNS = r"""
    (?(DEFINE)

        # For our purposes numbers are always positive and decimals.
        (?P<number> (?&open) (?: \d{1,3} (?: , \d{3} ){1,3} | \d+ )
            (?: \. \d+ )? (?&close) [*]? )

        # We also want to pull in number ranges when appropriate.
        (?P<range> (?&number) (?: \s* (?: - | to ) \s* (?&number) )? )

        # We also want to pull in number length x width.
        (?P<cross> (?&number) (?: \s* (?: x | by | \* ) \s* (?&number) )? )

        # Keywords that may precede a shorthand measurement
        (?P<shorthand_words> on \s* tag
                        | specimens?
                        | catalog
                        | measurements (?: \s+ [\p{Letter}]+)
                        | tag \s+ \d+ \s* =? (?: male | female)? \s* ,
                        | meas [.,]? (?: \s+ \w+ \. \w+ \. )?
        )

        # Common keyword misspellings preceding shorthand measurements
        (?P<shorthand_typos>  mesurements | Measurementsnt )

        # Keys where we need units to know if it's for mass or length
        (?P<key_units_req> measurements? | body | total )

        # Characters that separate shorthand values
        (?P<shorthand_sep> [:\/\-] )

        # Used in shorthand notation for unknown values
        (?P<shorthand_unknown> [\?x] )

    )"""

LENGTH_PATTERNS = r"""
    (?(DEFINE)

        # Length unit abbreviations
        (?P<len_units_abbrev> (?: [cm] (?&dot) m | in | ft ) (?&dot) s? )

        # Length unit words
        (?P<len_units_word>
            (?: meter
            | millimeter
            | centimeter
            | foot
            | feet
            | inch e? ) s? )

        # All length units
        (?P<len_units> (?&len_units_word) | (?&len_units_abbrev) )

        # Used for parsing forms like: 2 ft 4 inches
        (?P<len_foot> (?: foot | feet | ft ) s? (?&dot) )
        (?P<len_inch> (?: inch e? | in )     s? (?&dot) )

    )"""

MASS_PATTERNS = r"""
    (?(DEFINE)

        # Keywords for total mass
        (?P<total_wt_key>
            weightingrams | massingrams
            | (?: body | full | observed | total )
                (?&dot) \s* (?&wt_key_word)
        )

        #  Weight keyword
        (?P<wt_key_word>
            weights?
            | weigh (?: s | ed | ing )
            | mass
            | w (?&dot) t s? (?&dot) )

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

REPRODUCTIVE_PATTERNS = r"""
    (?(DEFINE)

        # Testes
        (?P<testes> \b (?: testes |  testis | testicles) \b )

        # Abbreviations for testes. Other indicators required
        (?P<testes_abbrev> \b (?: tes | ts | t) \b )

        # reproductive_data key
        (?P<reproductive_data> \b
            reproductive [\s_-]?
            (?: data | state | condition )
        \b )

    )"""
