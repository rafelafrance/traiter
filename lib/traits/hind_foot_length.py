"""Parse hind foot length notations."""

from pyparsing import Word, Regex
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

        parser.ignore(Word(stp.punct, excludeChars='"/'))
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
        return self.fix_up_double_quotes(text, result)
