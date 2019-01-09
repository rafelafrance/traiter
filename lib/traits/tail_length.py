"""Parse tail length notations."""

from pyparsing import Word
from lib.base_trait import BaseTrait
from lib.numeric_trait_mix_in import NumericTraitMixIn
import lib.shared_parser_patterns as sp


class TailLength(BaseTrait, NumericTraitMixIn):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        key_with_units = (
            sp.kwd('taillengthinmillimeters')
            | sp.kwd('taillengthinmm')
            | sp.kwd('tail length in millimeters')
            | sp.kwd('tail length in mm')
        )

        key = (
            sp.kwd('tail length')
            | sp.kwd('tail len')
            | sp.kwd('taillength')
            | sp.kwd('taillen')
            | sp.kwd('tail')
            | sp.kwd('tal')
        )

        parser = (
            key_with_units('units') + sp.pair
            | key + sp.pair + sp.len_units('units')
            | key + sp.pair
            | sp.shorthand_key + sp.shorthand
            | sp.shorthand
        )

        parser.ignore(Word(sp.punct))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()
        if parts.get('shorthand_tal') is not None:
            return self.shorthand_length(match, parts, 'shorthand_tal')
        return self.simple(match, parts)
