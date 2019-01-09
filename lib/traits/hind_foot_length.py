"""Parse hind foot length notations."""

from pyparsing import Word
from pyparsing import CaselessLiteral as lit
from lib.base_trait import BaseTrait
from lib.numeric_trait_mixin import NumericTraitMixIn
import lib.shared_trait_patterns as stp


class HindFootLength(NumericTraitMixIn, BaseTrait):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        key_with_units = (
            stp.kwd('hindfootlengthinmillimeters')
            | stp.kwd('hindfootlengthinmm')
            | stp.kwd('hindfoot length in millimeters')
            | stp.kwd('hindfoot length in mm')
        )

        key = (
            stp.kwd('hind foot with claw') | stp.kwd('hindfootwithclaw')
            | stp.kwd('hind foot length') | stp.kwd('hindfootlength')
            | stp.kwd('hind foot len') | stp.kwd('hindfootlen')
            | stp.kwd('hind_foot_length') | stp.kwd('hind_foot_len')
            | stp.kwd('hind foot') | stp.kwd('hindfoot')
            | lit('hfl') | lit('hf')
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
        if parts.get('shorthand_hfl') is not None:
            return self.shorthand_length(match, parts, 'shorthand_hfl')
        return self.simple(match, parts)
