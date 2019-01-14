"""Parse hind foot length notations."""

from pyparsing import Word, Regex
from pyparsing import CaselessKeyword as kwd
from lib.base_trait import BaseTrait
from lib.numeric_trait_mixin import NumericTraitMixIn
import lib.shared_trait_patterns as stp


class HindFootLength(NumericTraitMixIn, BaseTrait):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        key_with_units = (
            kwd('hindfootlengthinmillimeters')
            | kwd('hindfootlengthinmm')
            | kwd('hindfoot length in millimeters')
            | kwd('hindfoot length in mm')
        )

        key = (
            kwd('hind foot with claw') | kwd('hindfootwithclaw')
            | kwd('hind foot length') | kwd('hindfootlength')
            | kwd('hind foot len') | kwd('hindfootlen')
            | kwd('hind_foot_length') | kwd('hind_foot_len')
            | kwd('hind foot') | kwd('hindfoot')
            | Regex(r' \b hfl ', stp.flags) | Regex(r' \b hf ', stp.flags)
        )

        parser = (
            key_with_units('units') + stp.pair
            | key + stp.pair + stp.len_units('units')
            | key + stp.pair
            | key + stp.fraction + stp.len_units('units')
            | key + stp.fraction
            | stp.shorthand_key + stp.shorthand
            | stp.shorthand
        )

        parser.ignore(Word(stp.punct, excludeChars='/'))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()
        if parts.get('shorthand_hfl') is not None:
            return self.shorthand_length(match, parts, 'shorthand_hfl')
        if parts.get('numerator') is not None:
            return self.fraction(match, parts)
        return self.simple(match, parts)

    def fix_up_result(self, text, result):
        """Fix problematic parses."""
        return self.fix_up_inches(text, result)
