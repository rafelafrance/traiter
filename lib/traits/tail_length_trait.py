"""Parse tail length notations."""

import re
from functools import partial
from lib.traits.base_trait import BaseTrait
from lib.numeric_parser_mixin import NumericParserMixIn
import lib.shared_tokens as tkn


LOOKBACK = 40
IS_TESTES = re.compile(r' repoductive | gonad | test ', BaseTrait.flags)


class TailLengthTrait(NumericParserMixIn, BaseTrait):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        # Build the tokens
        self.kwd('key_with_units', r"""
            tail \s* len (?: gth )? \s* in \s*
            (?P<units> millimeters | mm ) """)

        self.lit('char_key', r' \b (?P<ambiguous_key> t ) (?! [a-z] )')

        self.kwd('keyword', r' tail \s* len (?: gth )? | tail | tal ')

        self.shared_token(tkn.len_units)
        self.shared_token(tkn.shorthand_key)
        self.shared_token(tkn.shorthand)
        self.shared_token(tkn.fraction)
        self.shared_token(tkn.pair)
        self.shared_token(tkn.triple)
        self.kwd('word', r' (?: [a-z] \w* ) ')
        self.lit('sep', r' [;,] | $ ')

        # Build rules for token replacement
        self.replace('key', ' keyword | char_key ')

        # Build rules for parsing the trait
        self.product(self.fraction, r"""
            key fraction (?P<units> len_units ) | key fraction """)

        self.product(self.simple, r"""
            key_with_units pair
            | key pair (?P<units> len_units )
            | key pair
            """)

        self.product(
            partial(self.shorthand_length, measurement='shorthand_tal'), r"""
            shorthand_key shorthand | shorthand
            | shorthand_key triple (?! shorthand | pair )
            """)

        self.finish_init()

    def fix_up_trait(self, trait, text):
        """Fix problematic parses."""
        if trait.ambiguous_key:
            start = max(0, trait.start - LOOKBACK)
            if IS_TESTES.search(text, start, trait.start):
                return None
            if len(text) > trait.end and text[trait.end].isalpha():
                return None

        return self.fix_up_inches(trait, text)
