"""Parse tail length notations."""

import re
from functools import partial
from lib.traits.numeric_trait import NumericTrait
import lib.shared_tokens as tkn


LOOKBACK_FAR = 40
LOOKBACK_NEAR = 20
IS_TESTES = re.compile(
    r' repoductive | gonad | test | scrot (?: al | um )? ',
    NumericTrait.flags)
IS_ELEVATION = re.compile(r' elev (?: ation )? ', NumericTrait.flags)
IS_TOTAL = re.compile(r' body | nose | snout ', NumericTrait.flags)
IS_TAG = re.compile(r' tag ', NumericTrait.flags)
IS_ID = re.compile(r' id (?: ent )? (?: ifier )? ', NumericTrait.flags)


class TailLengthTrait(NumericTrait):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self._build_token_rules()
        self._build_replace_rules()
        self._build_product_rules()

        self.finish_init()

    def _build_token_rules(self):
        self.shared_token(tkn.uuid)

        self.kwd('key_with_units', r"""
            tail \s* len (?: gth )? \s* in \s*
            (?P<units> millimeters | mm ) """)

        self.lit('char_key', r"""
            \b (?P<ambiguous_key> t ) (?! [a-z] ) (?! _ \D )
            """)

        self.kwd('keyword', r' tail \s* len (?: gth )? | tail | tal ')

        self.shared_token(tkn.len_units)
        self.shared_token(tkn.shorthand_key)
        self.shared_token(tkn.shorthand)
        self.shared_token(tkn.fraction)
        self.shared_token(tkn.pair)
        self.shared_token(tkn.triple)
        self.kwd('word', r' (?: [a-z] \w* ) ')
        self.lit('sep', r' [;,] | $ ')

    def _build_replace_rules(self):
        self.replace('key', ' keyword | char_key ')

    def _build_product_rules(self):
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

    def fix_up_trait(self, trait, text):
        """Fix problematic parses."""
        start = max(0, trait.start - LOOKBACK_NEAR)
        if IS_TOTAL.search(text, start, trait.start):
            return None

        if trait.ambiguous_key:
            start = max(0, trait.start - LOOKBACK_FAR)
            if IS_TESTES.search(text, start, trait.start) \
                    or IS_ELEVATION.search(text, start, trait.start) \
                    or IS_ID.search(text, start, trait.start):
                return None

            start = max(0, trait.start - LOOKBACK_NEAR)
            if IS_TAG.search(text, start, trait.start):
                return None

            if len(text) > trait.end and text[trait.end].isalpha():
                return None

        return self.fix_up_inches(trait, text)
