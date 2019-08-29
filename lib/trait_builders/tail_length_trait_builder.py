"""Parse tail length notations."""

import re
from functools import partial
from lib.trait_builders.numeric_trait_builder import NumericTraitBuilder
from lib.shared_tokens import SharedTokens


class TailLengthTraitBuilder(NumericTraitBuilder):
    """Parser logic."""

    # How far to look into the surrounding context to disambiguate the parse
    look_back_far = 40
    look_back_near = 20

    # These indicate that the parse is not really for a tail length
    is_testes = re.compile(
        ' reproductive | gonad | test | scrotal | scrotum | scrot ',
        NumericTraitBuilder.flags)
    is_elevation = re.compile(' elevation | elev ', NumericTraitBuilder.flags)
    is_total = re.compile(' body | nose | snout ', NumericTraitBuilder.flags)
    is_tag = re.compile(' tag ', NumericTraitBuilder.flags)
    is_id = re.compile(' identifier | ident | id ', NumericTraitBuilder.flags)

    def build_token_rules(self):
        """Define the tokens."""
        tkn = SharedTokens()

        self.copy(tkn['uuid'])  # UUIDs cause problems with numbers

        # Looking for keys like: tailLengthInMM
        self.keyword('key_with_units', r"""
            tail \s* ( length | len ) \s* in \s*
            (?P<units> millimeters | mm ) """)

        # The abbreviation key, just: t. This can be a problem.
        self.fragment('char_key', r"""
            \b (?P<ambiguous_key> t ) (?! [a-z] ) (?! _ \D )
            """)

        # Standard keywords that indicate a tail length follows
        self.keyword('keyword', [
            r' tail \s* length ',
            r' tail \s* len ',
            'tail',
            'tal'])

        # Units
        self.copy(tkn['len_units'])

        # Shorthand notation
        self.copy(tkn['shorthand_key'])
        self.copy(tkn['shorthand'])

        # Fractional numbers, like: 9/16
        self.copy(tkn['fraction'])

        # Possible pairs of numbers like: "10 - 20" or just "10"
        self.copy(tkn['range'])

        # Sometimes the last number is missing in the shorthand notation
        self.copy(tkn['triple'])

        # We allow random words in some situations
        self.keyword('word', r' ( [a-z] \w* ) ')

        # Some patterns require a separator
        self.fragment('sep', r' [;,] | $ ')

    def build_replace_rules(self):
        """Define rules for token simplification."""
        # Consider all of these tokens a key
        self.replace('key', 'keyword char_key'.split())

    def build_product_rules(self):
        """Define rules for output."""
        # Handle fractional values like: tailLength 9/16"
        self.product(self.fraction, [

            # E.g.: tail = 9/16 in
            'key fraction (?P<units> len_units )',

            # Without units, like: tail = 9/16
            'key fraction'])

        # A typical tail length notation
        self.product(self.simple, [

            # E.g.: tailLengthInMM=9-10
            'key_with_units range',

            # E.g.: tailLength=9-10 mm
            'key range (?P<units> len_units )',

            # Missing units like: tailLength 9-10
            'key range',
        ])

        self.product(
            partial(self.shorthand_length, measurement='shorthand_tal'), [
                'shorthand_key shorthand',  # With a key
                'shorthand',  # Without a key
                # Handle a truncated shorthand notation
                'shorthand_key triple (?! shorthand | range )'])

    def fix_problem_parses(self, trait, text):
        """Fix problematic parses."""
        # Check that this isn't a total length trait
        start = max(0, trait.start - self.look_back_near)
        if self.is_total.search(text, start, trait.start):
            return None

        # Problem parses happen mostly with an ambiguous key
        if trait.ambiguous_key:

            # Make sure this isn't a testes measurement
            start = max(0, trait.start - self.look_back_far)
            if self.is_testes.search(text, start, trait.start) \
                    or self.is_elevation.search(text, start, trait.start) \
                    or self.is_id.search(text, start, trait.start):
                return None

            # Make sure this isn't a tag
            start = max(0, trait.start - self.look_back_near)
            if self.is_tag.search(text, start, trait.start):
                return None

        # Try to disambiguate doubles quotes from inches
        return self.fix_up_inches(trait, text)
