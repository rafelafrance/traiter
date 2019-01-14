"""Parse ear length notations."""

from pyparsing import Word, Regex
from pyparsing import CaselessKeyword as kwd
from lib.base_trait import BaseTrait
from lib.numeric_trait_mixin import NumericTraitMixIn
import lib.shared_trait_patterns as stp


class EarLength(NumericTraitMixIn, BaseTrait):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        key_with_units = (
            kwd('earlengthinmillimeters')
            | kwd('earlengthinmm')
            | kwd('ear length in millimeters')
            | kwd('ear length in mm')
        )

        char_key = Regex(r""" \b e """, stp.flags)

        key = (
            kwd('ear from notch')
            | kwd('ear from crown')
            | kwd('ear length') | kwd('earlength')
            | kwd('ear')
            | char_key
        )

        parser = (
            key_with_units('units') + stp.pair
            | key + stp.fraction + stp.len_units('units')
            | key + stp.fraction
            | key + stp.pair + stp.len_units('units')
            | key + stp.pair
            | stp.shorthand_key + stp.shorthand
            | stp.shorthand
        )

        parser.ignore(Word(stp.punct, excludeChars='/'))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()
        if parts.get('shorthand_el') is not None:
            return self.shorthand_length(match, parts, 'shorthand_el')
        if parts.get('numerator') is not None:
            return self.fraction(match, parts)
        return self.simple(match, parts)

    def fix_up_result(self, text, result):
        """Fix problematic parses."""
        return self.fix_up_inches(text, result)
