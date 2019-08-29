"""Shared token patterns."""

from lib.util import ordinal, number_to_words
from stacked_regex.rule_builder import RuleBuilder


class SharedPatterns(RuleBuilder):
    """Build common reproductive trait tokens."""

    def __init__(self):
        """Build the stacked regular expressions."""
        super().__init__()
        self.numeric_tokens()
        self.misc_tokens()

    def numeric_tokens(self):
        """Build numeric parsing tokens."""
        self.fragment(
            'feet', r" foot s? | feet s? | ft s? (?! [,\w]) | (?<= \d ) ' ")

        # NOTE: Double quotes as inches is handled during fix up
        # The negative look-ahead is trying to distinguish between cases like
        # inTL with other words.
        self.fragment(
            'inches', ' ( inch e? s? | in s? ) (?! [a-dgi-km-ru-z] ) ')

        self.fragment(
            'metric_len', r' ( milli | centi )? meters? | ( [cm] [\s.]? m ) ')

        self.fragment(
            'len_units', '|'.join(
                [self[x].pattern for x in ('metric_len', 'feet', 'inches')]))
        len_units = self['len_units'].pattern

        self.fragment('pounds', r' pounds? | lbs? ')
        self.fragment('ounces', r' ounces? | ozs? ')
        self.fragment('metric_mass', r"""
            ( milligram | kilogram | gram ) ( s (?! [a-z]) )?
            | ( m \.? g | k \.? \s? g | g[mr]? )
                ( s (?! [a-z]) )?
            """)

        self.fragment('us_mass', '|'.join([
            self[x].pattern for x in ('pounds', 'ounces')]))

        self.fragment(
            'mass_units', '|'.join([
                self[x].pattern for x in ('metric_mass', 'pounds', 'ounces')]))
        mass_units = self['mass_units'].pattern

        # Numbers are positive decimals
        self.fragment('number', r"""
            ( \d{1,3} ( , \d{3} ){1,3} | \d+ ) ( \. \d+ )?
            | (?<= [^\d] ) \. \d+ | ^ \. \d+
            """)
        number = self['number'].pattern

        # A number or a range of numbers like "12 to 34" or "12.3-45.6"
        # Note we want to exclude dates and to not pick up partial dates
        # So: no part of "2014-12-11" would be in a range
        range_joiner = r'- | to'
        self.fragment('range_joiner', range_joiner)
        self.fragment('range', fr"""
            (?<! \d ) (?<! \d [|,.#+-] ) (?<! \b to \s ) (?<! [#] )
            (?P<estimated_value> \[ \s* )?
            (?P<value1> {number} )
            \]? \s*?
            ( \s* ( {range_joiner} ) \s* (?P<value2> {number} ) )?
            (?! \d+ | [|,.+-] \d | \s+ to \b )
            """)

        # A number times another number like: "12 x 34" this is typically
        # length x width. We Allow a triple like "12 x 34 x 56" but we ony take
        # the first two numbers
        cross_joiner = r' ( x | by | \* | - ) '
        self.fragment('cross_joiner', cross_joiner)
        self.fragment('cross', fr"""
            (?<! [\d/,.-]\d ) (?<! \b by )
            (?P<estimated_value> \[ \s* )?
            (?P<value1> {number} ) \s*
            \]? \s*?
            ( (?P<units1> {len_units})
                    \s* {cross_joiner}
                    \s* (?P<value2> {number}) \s* (?P<units2> {len_units})
                | {cross_joiner}
                    \s* (?P<value2> {number}) \s* (?P<units1> {len_units})
                | {cross_joiner}
                    \s* (?P<value2> {number}) \b (?! {mass_units})
                | (?P<units1> {len_units})
                | \b (?! {mass_units})
            )""")

        # For fractions like "1 2/3" or "1/2".
        # We don't allow dates like "1/2/34".
        self.fragment('fraction', r"""
            (?<! [\d/,.] )
            (?P<whole> \d+ \s+ )? (?P<numerator> \d+ ) / (?P<denominator> \d+ )
            (?! [\d/,.] )
            """)

        # This is a common notation: "11-22-33-44:99g".
        # There are other separators "/", ":", etc.
        # There is also an extended form that looks like:
        #   "11-22-33-44-fa55-hb66:99g" There may be several extended numbers.
        #
        #   11 = total length (ToL or TL) or sometimes head body length
        #   22 = tail length (TaL)
        #   33 = hind foot length (HFL)
        #   44 = ear length (EL)
        #   99 = body mass is optional, as is the mass units
        #
        # Unknown values are filled with "?" or "x".
        #   E.g.: "11-x-x-44" or "11-?-33-44"
        #
        # Ambiguous measurements are enclosed in brackets.
        #   E.g.: 11-[22]-33-[44]:99g

        self.fragment('shorthand_key', r"""
            on \s* tag | specimens? | catalog
            | ( measurement s? | meas ) [:.,]{0,2} ( \s* length \s* )?
                ( \s* [({\[})]? [a-z]{1,2} [)}\]]? \.? )?
            | tag \s+ \d+ \s* =? ( male | female)? \s* ,
            | measurements? | mesurements? | measurementsnt
            """)

        # A possibly unknown value
        self.fragment('sh_num', r""" \d+ ( \. \d+ )? | (?<= [^\d] ) \. \d+ """)
        sh_num = self['sh_num'].pattern
        self.fragment('sh_val', f' ( {sh_num} | [?x]{{1,2}} | n/?d ) ')
        sh_val = self['sh_val'].pattern

        self.fragment('shorthand', fr"""
            (?<! [\d/a-z-] )
            (?P<shorthand_tl> (?P<estimated_tl> \[ )? {sh_val} \]? )
            (?P<shorthand_sep> [:/-] )
            (?P<shorthand_tal> (?P<estimated_tal> \[ )? {sh_val} \]? )
            (?P=shorthand_sep)
            (?P<shorthand_hfl> (?P<estimated_hfl> \[ )? {sh_val} \]? )
            (?P=shorthand_sep)
            (?P<shorthand_el> (?P<estimated_el> \[ )? {sh_val} \]? )
            (?P<shorthand_ext> ( (?P=shorthand_sep) [a-z]{{1,4}} {sh_val} )* )
            ( [\s=:/-] \s*
                (?P<estimated_wt> \[? \s* )
                (?P<shorthand_wt> {sh_val} ) \s*
                \]?
                (?P<shorthand_wt_units> {self['metric_mass'].pattern} )?
                \s*? \]?
            )?
            (?! [\d/:=a-z-] )
            """)

        # Sometimes the last number is missing. Be careful to not pick up dates.
        self.fragment('triple', fr"""
            (?<! [\d/a-z-] )
            (?P<shorthand_tl> (?P<estimated_tl> \[ )? {sh_val} \]? )
            (?P<shorthand_sep> [:/-] )
            (?P<shorthand_tal> (?P<estimated_tal> \[ )? {sh_val} \]? )
            (?P=shorthand_sep)
            (?P<shorthand_hfl> (?P<estimated_hfl> \[ )? {sh_val} \]? )
            (?! [\d/:=a-z-] )
            """)

    def misc_tokens(self):
        """Setup common token patterns."""
        # UUIDs cause problems when extracting certain shorthand notations.
        self.fragment('uuid', r"""
            \b [0-9a-f]{8} - [0-9a-f]{4} - [1-5][0-9a-f]{3}
                - [89ab][0-9a-f]{3} - [0-9a-f]{12} \b """)

        # Some numeric values are reported as ordinals or words
        ordinals = [ordinal(x) for x in range(1, 6)]
        ordinals += [number_to_words(x) for x in ordinals]
        self.fragment('ordinals', ' | '.join([x for x in ordinals]))

        # Time units
        self.fragment(
            'time_units', r'years? | months? | weeks? | days? | hours?')

        # Side keywords
        self.fragment('side', r"""
            [/(\[] \s* (?P<side> [lr] \b ) \s* [)\]]? 
            | (?P<side> both | left | right | lft | rt | [lr] \b ) """)

        self.fragment('dimension', r' (?P<dimension> length | width ) ')

        # Numeric sides interfere with number parsing so combine \w dimension
        self.fragment(
            'dim_side',
            fr""" {self['dimension'].pattern} \s* (?P<side> [12] ) \b """)

        self.fragment(
            'cyst',
            r""" (\d+ \s+)?
                (cyst s? | bodies | cancerous | cancer )
                ( \s+ ( on | in ))?""")

        # integers, no commas or signs and typically small
        self.fragment('integer', r""" \d+ (?! [%\d\-] ) """)
