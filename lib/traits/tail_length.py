"""Parse tail length notations."""

from pyparsing import Word
from lib.base_trait import BaseTrait
from lib.numeric_trait_mixin import NumericTraitMixIn
import lib.shared_trait_patterns as stp


class TailLength(NumericTraitMixIn, BaseTrait):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        key_with_units = (
            stp.kwd('taillengthinmillimeters')
            | stp.kwd('taillengthinmm')
            | stp.kwd('tail length in millimeters')
            | stp.kwd('tail length in mm')
        )

        key = (
            stp.kwd('tail length')
            | stp.kwd('tail len')
            | stp.kwd('taillength')
            | stp.kwd('taillen')
            | stp.kwd('tail')
            | stp.kwd('tal')
        )

        parser = (
            key_with_units('units') + stp.pair
            | key + stp.pair + stp.len_units('units')
            | key + stp.pair
            | stp.shorthand_key + stp.shorthand
            | stp.shorthand
        )

        parser.ignore(Word(stp.punct))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()
        if parts.get('shorthand_tal') is not None:
            return self.shorthand_length(match, parts, 'shorthand_tal')
        return self.simple(match, parts)
