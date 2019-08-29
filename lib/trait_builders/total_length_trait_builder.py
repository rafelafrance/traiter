"""Parse total length notations."""

import re
from functools import partial
from lib.trait_builders.numeric_trait_builder import NumericTraitBuilder
from lib.shared_tokens import SharedTokens


class TotalLengthTraitBuilder(NumericTraitBuilder):
    """Parser logic."""

    # How far to look into the surrounding context to disambiguate the parse
    look_back_far = 40
    look_back_near = 10

    # These indicate that the parse is not a total length
    is_id = re.compile(
        ' identifier | ident | id | collector ',
        NumericTraitBuilder.flags)
    is_trap = re.compile(' trap ', NumericTraitBuilder.flags)
    is_testes = re.compile(
        ' reproductive | gonad | test | scrotal | scrotum | scrot ',
        NumericTraitBuilder.flags)

    # The 'L' abbreviation gets confused with abbreviation for Left sometimes.
    # Try to disambiguate the two by looking for a Right near by.
    look_around = 10
    is_left = re.compile(r' \b r \b ', NumericTraitBuilder.flags)

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self.build_token_rules()
        self.build_product_rules()

        self.compile_regex()

    def build_token_rules(self):
        """Define the tokens."""
        tkn = SharedTokens()

        # Units are in the key, like: TotalLengthInMillimeters
        self.keyword('key_with_units', r"""
            ( total | snout \s* vent | head \s* body | fork ) \s*
            ( length | len )? \s* in \s* (?P<units> millimeters | mm )
            """)

        # Various total length keys
        self.fragment('key', [

            # E.g.: total-length-in
            r'total  [\s-]* length [\s-]* in',

            # E.g.: standardLengths
            r'( total | max | standard ) [\s-]* lengths? \b',

            # E.g.: Meas: length (L):
            r'meas [\s*:]? \s* length [\s(]* [l] [)\s:]*',

            # E.g.: measured: L
            r'meas ( [a-z]* )? \.? : \s* l (?! [a-z.] )',

            # E.g.: tol_
            r't [o.]? \s? l \.? \s? _? (?! [a-z.] )',

            # E.g.: s.l.
            r's \.? \s? l \.? (?! [a-z.] )',

            # E.g.: label length
            r'label [\s.]* lengths? \b',

            # E.g.: fork-length
            r'( fork | mean | body ) [\s-]* lengths? \b',

            # E.g.: s.v.l.
            r's \.? \s? v \.? \s? l \.? (?! [a-z.] )',

            # E.g.: snout-vent-length
            r'snout [\s-]* vent [\s-]* lengths? \b',
        ])

        # Words that indicate we don't have a total length
        self.keyword('skip', 'horns?')

        # The word length on its own. Make sure it isn't proceeded by a letter
        self.fragment('ambiguous', r'(?<! [a-z] )(?<! [a-z] \s ) lengths? ')

        # We don't know if this is a length until we see the units
        self.fragment('key_units_req', 'measurements? body total'.split())

        # Units
        self.copy(tkn['metric_len'])
        self.copy(tkn['feet'])
        self.copy(tkn['inches'])

        # Shorthand notation
        self.copy(tkn['shorthand_key'])
        self.copy(tkn['shorthand'])
        self.copy(tkn['triple'])  # Truncated shorthand

        # Fractional numbers, like: 9/16
        self.copy(tkn['fraction'])

        # Possible range of numbers like: "10 - 20" or just "10"
        self.copy(tkn['range'])

        # The abbreviation key, just: t. This can be a problem.
        self.fragment('char_key', r' \b (?P<ambiguous_key> l ) (?= [:=-] ) ')

        # We allow random words in some situations
        self.keyword('word', r' ( [a-z] \w* ) ')

        # Some patterns require a separator
        self.fragment('semicolon', r' [;] | $ ')
        self.fragment('comma', r' [,] | $ ')

    def build_product_rules(self):
        """Define rules for output."""
        # Handle fractional values like: total length 9/16"
        self.product(self.fraction, [

            # E.g.: total = 9/16 inches
            'key_units_req fraction (?P<units> metric_len | feet | inches )',

            # E.g.: svl 9/16 inches
            'key fraction (?P<units> metric_len | feet | inches )',

            # E.g.: len 9/16 in
            """(?P<ambiguous_key> ambiguous) fraction
                (?P<units> metric_len | feet | inches )""",
            ])

        self.product(partial(self.compound, units=['ft', 'in']), [

            # E.g.: total length 4 feet 7 inches
            'key (?P<ft> range) feet ( comma )? (?P<in> range) inches',

            # E.g.: length 4 ft 7 in
            """(?P<ambiguous_key>
                (?P<ft> range) feet ( comma )? (?P<in> range) inches )""",
        ])

        # A typical total length notation
        self.product(self.simple, [

            # E.g.: total length in mm 10 - 13
            'key_with_units range',

            # E.g.: tag 10-20-39 10 - 13 in
            """shorthand_key ( triple )? range
                (?P<units> metric_len | feet | inches )""",

            # E.g.: tag 10-20-39 cm 10-12
            'shorthand_key ( triple )? (?P<units> metric_len ) range',

            # E.g.: total 10/20/30 10 to 12 cm
            """key_units_req ( triple )? range
                (?P<units> metric_len | feet | inches )""",

            # E.g.: 10 to 11 inches TL
            'range (?P<units> metric_len | feet | inches ) key',

            # E.g.: total 10-20-40 10 to 20 inches ToL
            """ambiguous ( triple )? range
                (?P<units> metric_len | feet | inches ) key""",

            # E.g.: total 10-20-40 10 to 20 ToL
            'ambiguous ( triple )? range key',

            # E.g.: length 10 to 11 inches
            """(?P<ambiguous_key> ambiguous) range
                (?P<units> metric_len | feet | inches )""",

            # E.g.: length feet 10 to 11
            """(?P<ambiguous_key> ambiguous)
                (?P<units> metric_len | feet | inches ) range""",

            # E.g.: length 10 to 11
            '(?P<ambiguous_key> ambiguous) range',

            # E.g.: SVL 10-11 cm
            'key range (?P<units> metric_len | feet | inches )',

            # E.g.: forkLen cm 10-11
            'key (?P<units> metric_len | feet | inches ) range',

            # E.g.: total length: 10-29-39 10-11
            'key ( triple )? range',

            # E.g.: head body length is a whopping 12.4 meters
            """key ( word | semicolon | comma ){1,3} range
                (?P<units> metric_len | feet | inches )""",

            # E.g.: SVL is 10-12
            'key ( word | semicolon | comma ){1,3} range',

            # E.g.: L 12.4 cm
            'char_key range (?P<units> metric_len | feet | inches )',

            # E.g.: L 12.4
            'char_key range',
        ])

        self.product(
            partial(self.shorthand_length, measurement='shorthand_tl'), [
                '( shorthand_key | key_units_req ) shorthand',  # With a key
                'shorthand',                                    # Without a key
                # Handle a truncated shorthand notation
                """( shorthand_key | key_units_req ) triple
                    (?! shorthand | range )""",
            ])

    def fix_problem_parses(self, trait, text):
        """Fix problematic parses."""

        # Handle IDs
        start = max(0, trait.start - self.look_back_far)
        if self.is_id.search(text, start, trait.start):
            return None

        # Handle traps, like: trap TL01
        start = max(0, trait.start - self.look_back_near)
        if self.is_trap.search(text, start, trait.start):
            return None

        # Problem parses often happen with an ambiguous key
        if trait.ambiguous_key:

            # Testes measurement may involve an "L"
            start = max(0, trait.start - self.look_around)
            end = min(len(text), trait.end + self.look_around)
            if self.is_testes.search(text, start, trait.start):
                return None

            # Make sure the "L" isn't for "left"
            if self.is_left.search(text, start, trait.start):
                return None
            if self.is_left.search(text, trait.end, end):
                return None

        # Try to disambiguate doubles quotes from inches
        return self.fix_up_inches(trait, text)
