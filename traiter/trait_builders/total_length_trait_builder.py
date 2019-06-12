"""Parse total length notations."""

import re
from functools import partial
from traiter.trait_builders.numeric_trait_builder import NumericTraitBuilder
import traiter.shared_tokens as tkn


class TotalLengthTraitBuilder(NumericTraitBuilder):
    """Parser logic."""

    # How far to look into the surrounding context to disambiguate the parse
    look_back_far = 40
    look_back_near = 10

    # These indicate that the parse is not a total length
    is_id = re.compile(
            r' identifier | ident | id | collector ',
            NumericTraitBuilder.flags)
    is_trap = re.compile(r' trap ', NumericTraitBuilder.flags)
    is_testes = re.compile(
            r' reproductive | gonad | test | scrotal | scrotum | scrot ',
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
        self.shared_token(tkn.uuid)

        # Words that indicate we don't have a total length
        self.keyword('skip', 'horns?')

        # Units are in the key, like: TotalLengthInMillimeters
        self.keyword('key_with_units', r"""
            ( total | snout \s* vent | head \s* body | fork ) \s*
            ( length | len )? \s* in \s* (?P<units> millimeters | mm )
            """)

        # Various total length keys
        self.fragment('key', [

            # Like: total-length-in
            r'total  [\s-]* length [\s-]* in',

            # Like: standardLengths
            r'( total | max | standard ) [\s-]* lengths? \b',

            # Like: Meas: length (L):
            r'meas [\s*:]? \s* length [\s(]* [l] [)\s:]*',

            # Like: measured: L
            r'meas ( [a-z]* )? \.? : \s* l (?! [a-z.] )',

            # Like: tol_
            r't [o.]? \s? l \.? \s? _? (?! [a-z.] )',

            # Like: s.l.
            r's \.? \s? l \.? (?! [a-z.] )',

            # Like: label length
            r'label [\s.]* lengths? \b',

            # Like: fork-length
            r'( fork | mean | body ) [\s-]* lengths? \b',

            # Like: s.v.l.
            r's \.? \s? v \.? \s? l \.? (?! [a-z.] )',

            # Like: snout-vent-length
            r'snout [\s-]* vent [\s-]* lengths? \b',
        ])

        # The word length on its own. Make sure it isn't proceeded by a letter
        self.fragment('ambiguous', r'(?<! [a-z] )(?<! [a-z] \s ) lengths? ')

        # A length that is a total length if we have units
        self.fragment('key_units_req', 'measurements? body total'.split())

        # Units
        self.shared_token(tkn.metric_len)
        self.shared_token(tkn.feet)
        self.shared_token(tkn.inches)

        # Shorthand notation
        self.shared_token(tkn.shorthand_key)
        self.shared_token(tkn.shorthand)
        self.shared_token(tkn.triple)  # Truncated shorthand

        # Fractional numbers, like: 9/16
        self.shared_token(tkn.fraction)

        # Possible pairs of numbers like: "10 - 20" or just "10"
        self.shared_token(tkn.pair)

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

            'key_units_req fraction (?P<units> metric_len | feet | inches )',

            'key fraction (?P<units> metric_len | feet | inches )',

            """(?P<ambiguous_key> ambiguous) fraction
                (?P<units> metric_len | feet | inches )""",
            ])

        self.product(partial(self.compound, units=['ft', 'in']), [

            'key (?P<ft> pair) feet ( comma )? (?P<in> pair) inches',

            """(?P<ambiguous_key>
                (?P<ft> pair) feet ( comma )? (?P<in> pair) inches )""",
        ])

        self.product(self.simple, [
            'key_with_units pair',

            """shorthand_key ( triple )? pair
                (?P<units> metric_len | feet | inches )""",

            'shorthand_key ( triple )? (?P<units> metric_len ) pair',

            """key_units_req ( triple )? pair
                (?P<units> metric_len | feet | inches )""",

            'pair (?P<units> metric_len | feet | inches ) key',

            """ambiguous ( triple )? pair
                (?P<units> metric_len | feet | inches ) key""",

            'ambiguous ( triple )?  pair key',

            """(?P<ambiguous_key> ambiguous) pair
                (?P<units> metric_len | feet | inches )""",

            """(?P<ambiguous_key> ambiguous)
                (?P<units> metric_len | feet | inches ) pair""",

            '(?P<ambiguous_key> ambiguous) pair',

            'key pair (?P<units> metric_len | feet | inches )',

            'key (?P<units> metric_len | feet | inches ) pair',

            'key ( triple )? pair',

            """key ( word | semicolon | comma ){1,3} pair
                (?P<units> metric_len | feet | inches )""",

            'key ( word | semicolon | comma ){1,3} pair',

            'char_key pair (?P<units> metric_len | feet | inches )',

            'char_key pair',
        ])

        self.product(
            partial(self.shorthand_length, measurement='shorthand_tl'), [

                '( shorthand_key | key_units_req ) shorthand | shorthand',

                """( shorthand_key | key_units_req ) triple 
                    (?! shorthand | pair )""",
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
