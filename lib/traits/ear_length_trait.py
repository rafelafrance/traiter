"""Parse ear length notations."""

import re
from functools import partial
from lib.traits.numeric_trait import NumericTrait
import lib.shared_tokens as tkn


LOOKBACK_FAR = 40
LOOKBACK_NEAR = 10
IS_ET = re.compile(r' e \.? t ', NumericTrait.flags)
IS_NUMBER = re.compile(r' [#] ', NumericTrait.flags)
IS_MAG = re.compile(r' magnemite', NumericTrait.flags)

LOOKAHEAD_NEAR = 5
IS_EAST = re.compile(r' \b n ', NumericTrait.flags)


class EarLengthTrait(NumericTrait):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)
        self.shared_token(tkn.uuid)

        # Build the tokens
        self.kwd('key_with_units', r"""
            ear \s* len (?: gth )? \s* in \s* (?P<units> millimeters | mm )
            """)

        self.lit('char_measured_from', r"""
            (?<! [a-z] ) (?<! [a-z] \s )
            (?P<ambiguous_key> e ) /? (?P<measured_from> n | c )
            (?! \.? [a-z] )
            """)

        self.lit('char_key', r"""
            (?<! \w ) (?<! \w \s )
            (?P<ambiguous_key> e )
            (?! \.? \s? [a-z\(] )
            """)

        self.kwd('keyword', r"""
            ear \s* from \s* (?P<measured_from> notch | crown )
            | ear \s* len (?: gth )?
            | ear (?! \s* tag )
            | ef (?P<measured_from> n | c )
            """)

        self.shared_token(tkn.len_units)
        self.shared_token(tkn.fraction)
        self.shared_token(tkn.shorthand_key)
        self.shared_token(tkn.shorthand)
        self.shared_token(tkn.pair)
        self.kwd('word', r' (?: [a-z] \w* ) ')
        self.lit('sep', r' [;,] | $ ')

        # Build rules for token replacement
        self.replace('key', ' keyword | char_key | char_measured_from ')

        # Build rules for parsing the trait
        self.product(self.fraction, r"""
            key fraction (?P<units> len_units ) | key fraction """)

        self.product(self.simple, r"""
            key_with_units pair
            | key pair (?P<units> len_units )
            | key pair
            """)

        self.product(
            partial(self.shorthand_length, measurement='shorthand_el'),
            r' shorthand_key shorthand | shorthand ')

        self.finish_init()

    def fix_up_trait(self, trait, text):
        """Fix problematic parses."""
        if trait.ambiguous_key:
            start = max(0, trait.start - LOOKBACK_NEAR)
            if IS_ET.search(text, start, trait.start):
                return None
            if IS_NUMBER.search(text, start, trait.start):
                return None

            start = max(0, trait.start - LOOKBACK_FAR)
            if IS_MAG.search(text, start, trait.start):
                return None

            end = min(len(text), trait.end + LOOKAHEAD_NEAR)
            if IS_EAST.search(text, trait.end, end):
                return None

        return self.fix_up_inches(trait, text)
