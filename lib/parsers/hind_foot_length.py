"""Parse hind foot length notations."""

from functools import partial
from lib.parsers.base import Base
from lib.parsers.numeric_parser_mixin import NumericParserMixIn
import lib.parsers.shared_tokens as tkn


class HindFootLength(NumericParserMixIn, Base):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        # Build the tokens
        self.kwd('key_with_units', r"""
            (?: hind \s* )? foot \s* len (?: gth )? \s* in \s*
            (?P<units> millimeters | mm ) """)

        self.kwd('key', r"""
            hind \s* foot \s* with \s* (?P<includes> claw )
            | hind \s* foot (?: \s* len (?: gth )? )?
            | \b hfl | \b hf """)

        self.shared_token(tkn.len_units)
        self.shared_token(tkn.shorthand_key)
        self.shared_token(tkn.shorthand)
        self.shared_token(tkn.fraction)
        self.shared_token(tkn.pair)
        self.shared_token(tkn.triple)
        self.kwd('word', r' (?: [a-z] \w* ) ')
        self.lit('sep', r' [;,] | $ ')

        # Build rules for parsing the trait
        self.product(self.fraction, r"""
            key fraction (?P<units> len_units ) | key fraction """)

        self.product(self.simple, r"""
            key_with_units pair
            | key pair (?P<units> len_units )
            | key pair
            """)

        self.product(
            partial(self.shorthand_length, measurement='shorthand_hfl'), r"""
            shorthand_key shorthand | shorthand
            | shorthand_key triple (?! shorthand | pair )
            """)

        self.finish_init()

    def fix_up_trait(self, trait, text):
        """Fix problematic parses."""
        return self.fix_up_inches(trait, text)
