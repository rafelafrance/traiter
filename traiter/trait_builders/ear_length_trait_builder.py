"""Parse ear length notations."""

import re
from functools import partial
from traiter.trait_builders.numeric_trait_builder import NumericTraitBuilder
import traiter.shared_tokens as tkn


class EarLengthTraitBuilder(NumericTraitBuilder):
    """Parser logic."""

    # How far to look into the surrounding context to disambiguate the parse
    look_back_far = 40
    look_back_near = 10

    # These indicate that the parse is not really for an ear length
    is_et = re.compile(r' e \.? t ', NumericTraitBuilder.flags)
    is_number = re.compile(' [#] ', NumericTraitBuilder.flags)
    is_mag = re.compile(' magnemite ', NumericTraitBuilder.flags)
    is_id = re.compile(' identifier | ident | id ', NumericTraitBuilder.flags)

    # The 'E' abbreviation gets confused with abbreviation for East sometimes.
    # Try to disambiguate the two by looking for a North near by.
    look_around = 10
    is_east = re.compile(r' \b n ', NumericTraitBuilder.flags)

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self.build_token_rules()
        self.build_replace_rules()
        self.build_product_rules()

        self.compile_regex()

    def build_token_rules(self):
        """Define the tokens."""
        self.shared_token(tkn.uuid)  # UUIDs cause problems with shorthand

        # Units are in the key, like: EarLengthInMillimeters
        self.keyword('key_with_units', r"""
            ear \s* ( length | len ) \s* in \s* (?P<units> millimeters | mm )
            """)

        # Abbreviation containing the measured from notation, like: e/n or e/c
        self.fragment('char_measured_from', r"""
            (?<! [a-z] ) (?<! [a-z] \s )
            (?P<ambiguous_key> e ) /? (?P<measured_from> n | c )
            (?! \.? [a-z] )
            """)

        # The abbreviation key, just: e. This can be a problem.
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

            # E.g.: ear = 9/16 in
            'key fraction (?P<units> len_units )',

            # Without units, like: ear = 9/16
            'key fraction',
        ])

        # A typical ear length notation
        self.product(self.simple, [

            # E.g.: earLengthInMM 9-10
            'key_with_units pair',

            # E.g.: ear 9-10 mm
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
        # Problem parses happen mostly with an ambiguous key
        if trait.ambiguous_key:

            # "E.T." is not an ear length measurement
            start = max(0, trait.start - self.look_back_near)
            if self.is_et.search(text, start, trait.start) \
                    or self.is_number.search(text, start, trait.start):
                return None

            # Magnemite confounds the abbreviation
            start = max(0, trait.start - self.look_back_far)
            if self.is_mag.search(text, start, trait.start) \
                    or self.is_id.search(text, start, trait.start):
                return None

            # Make sure it's not actually an abbreviation for "East"
            start = max(0, trait.start - self.look_around)
            end = min(len(text), trait.end + self.look_around)
            if self.is_east.search(text, start, trait.start) \
                    or self.is_east.search(text, trait.end, end):
                return None

        # Try to disambiguate doubles quotes from inches
        return self.numeric_fix_ups(trait, text)
