"""Parse tail length notations."""

import re
from functools import partial
from traiter.trait_builders.numeric_trait_builder import NumericTraitBuilder
import traiter.shared_tokens as tkn


LOOK_BACK_FAR = 40
LOOK_BACK_NEAR = 20
IS_TESTES = re.compile(
    r' reproductive | gonad | test | scrotal | scrotum | scrot ',
    NumericTraitBuilder.flags)
IS_ELEVATION = re.compile(r' elevation | elev ', NumericTraitBuilder.flags)
IS_TOTAL = re.compile(r' body | nose | snout ', NumericTraitBuilder.flags)
IS_TAG = re.compile(r' tag ', NumericTraitBuilder.flags)
IS_ID = re.compile(r' identifier | ident | id ', NumericTraitBuilder.flags)


class TailLengthTraitBuilder(NumericTraitBuilder):
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

        self.keyword('key_with_units', r"""
            tail \s* ( length | len ) \s* in \s*
            (?P<units> millimeters | mm ) """)

        self.fragment('char_key', r"""
            \b (?P<ambiguous_key> t ) (?! [a-z] ) (?! _ \D )
            """)

        self.keyword('keyword', r' tail \s* length | len | tail | tal ')

        self.shared_token(tkn.len_units)
        self.shared_token(tkn.shorthand_key)
        self.shared_token(tkn.shorthand)
        self.shared_token(tkn.fraction)
        self.shared_token(tkn.pair)
        self.shared_token(tkn.triple)
        self.keyword('word', r' ( [a-z] \w* ) ')
        self.fragment('sep', r' [;,] | $ ')

    def build_replace_rules(self):
        """Define rules for token simplification."""
        self.replace('key', ['keyword', 'char_key'])

    def build_product_rules(self):
        """Define rules for output."""
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

    def fix_problem_parses(self, trait, text):
        """Fix problematic parses."""
        start = max(0, trait.start - LOOK_BACK_NEAR)
        if IS_TOTAL.search(text, start, trait.start):
            return None

        if trait.ambiguous_key:
            start = max(0, trait.start - LOOK_BACK_FAR)
            if IS_TESTES.search(text, start, trait.start) \
                    or IS_ELEVATION.search(text, start, trait.start) \
                    or IS_ID.search(text, start, trait.start):
                return None

            start = max(0, trait.start - LOOK_BACK_NEAR)
            if IS_TAG.search(text, start, trait.start):
                return None

            if len(text) > trait.end and text[trait.end].isalpha():
                return None

        return self.fix_up_inches(trait, text)
