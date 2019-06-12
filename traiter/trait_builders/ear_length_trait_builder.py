"""Parse ear length notations."""

import re
from functools import partial
from traiter.trait_builders.numeric_trait_builder import NumericTraitBuilder
import traiter.shared_tokens as tkn


LOOK_BACK_FAR = 40
LOOK_BACK_NEAR = 10
IS_ET = re.compile(r' e \.? t ', NumericTraitBuilder.flags)
IS_NUMBER = re.compile(r' [#] ', NumericTraitBuilder.flags)
IS_MAG = re.compile(r' magnemite ', NumericTraitBuilder.flags)
IS_ID = re.compile(r' identifier | ident | id ', NumericTraitBuilder.flags)

LOOK_AROUND = 10
IS_EAST = re.compile(r' \b n ', NumericTraitBuilder.flags)


class EarLengthTraitBuilder(NumericTraitBuilder):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self.build_token_rules()
        self.build_replace_rules()
        self.build_product_rules()

        self.compile_regex()

    def build_token_rules(self):
        """Define the tokens."""
        self.shared_token(tkn.uuid)

        # Units are in the key, like: earlengthinmillimeters
        self.keyword('key_with_units', r"""
            ear \s* ( length | len ) \s* in \s* (?P<units> millimeters | mm )
            """)

        # Abbreviation containing the measured from notation, like: e/n or e/c
        self.fragment('char_measured_from', r"""
            (?<! [a-z] ) (?<! [a-z] \s )
            (?P<ambiguous_key> e ) /? (?P<measured_from> n | c )
            (?! \.? [a-z] )
            """)

        # The abbreviation key, just: e. This can be a problem
        self.fragment('char_key', r"""
            (?<! \w ) (?<! \w \s )
            (?P<ambiguous_key> e )
            (?! \.? \s? [a-z\(] )
            """)

        # Standard keywords that indicate an ear length follows
        self.keyword('keyword', [
            r' ear \s* from \s* (?P<measured_from> notch | crown )',
            r' ear \s* ( length | len )',
            r' ear (?! \s* tag )',
            r' ef (?P<measured_from> n | c )',
            ])

        # Units
        self.shared_token(tkn.len_units)

        # Fractional numbers, like: 9/16
        self.shared_token(tkn.fraction)

        # Shorthand notation
        self.shared_token(tkn.shorthand_key)
        self.shared_token(tkn.shorthand)

        # Possible pairs of numbers like: "10 - 20" or just "10"
        self.shared_token(tkn.pair)

        # We allow random words in some situations
        self.keyword('word', r' ( [a-z] \w* ) ')

        # Some patterns require a separator
        self.fragment('sep', r' [;,] | $ ')

    def build_replace_rules(self):
        """Define rules for token simplification."""
        # Consider any of the following as just a key
        self.replace('key', [
            'keyword',
            'char_key',
            'char_measured_from',
        ])

    def build_product_rules(self):
        """Define rules for output."""
        # Handle fractional values like: ear 9/16"
        self.product(self.fraction, [

            # Like: ear = 9/16 inches
            'key fraction (?P<units> len_units )',

            # Like: ear = 9/16
            'key fraction',
        ])

        # A typical ear length notation
        self.product(self.simple, [

            # Like: earlengthinmmm 9-10
            'key_with_units pair',

            # Like: ear 9-10 mm
            'key pair (?P<units> len_units )',

            # Missing units like: ear: 9-10
            'key pair',
        ])

        # Shorthand notation like: on tag: 11-22-33-44=99g
        self.product(
            partial(self.shorthand_length, measurement='shorthand_el'), [
                'shorthand_key shorthand',  # With a key
                'shorthand',                # Without a key
            ])

    def fix_problem_parses(self, trait, text):
        """Fix problematic parses."""
        if trait.ambiguous_key:
            start = max(0, trait.start - LOOK_BACK_NEAR)
            if IS_ET.search(text, start, trait.start) \
                    or IS_NUMBER.search(text, start, trait.start):
                return None

            start = max(0, trait.start - LOOK_BACK_FAR)
            if IS_MAG.search(text, start, trait.start) \
                    or IS_ID.search(text, start, trait.start):
                return None

            start = max(0, trait.start - LOOK_AROUND)
            end = min(len(text), trait.end + LOOK_AROUND)
            if IS_EAST.search(text, start, trait.start) \
                    or IS_EAST.search(text, trait.end, end):
                return None

        return self.numeric_fix_ups(trait, text)
