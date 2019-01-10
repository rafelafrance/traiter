"""Parse tail length notations."""

import re
from pyparsing import Word, Regex
from lib.base_trait import BaseTrait
from lib.numeric_trait_mixin import NumericTraitMixIn
import lib.shared_trait_patterns as stp


LOOKBACK = 40
IS_TESTES = re.compile(r' repoductive | gonad | test ', stp.flags)
IS_CROSS = re.compile(stp.cross_re, stp.flags)


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

        char_key = Regex(r""" \b t """, stp.flags)

        key = (
            stp.kwd('tail length')
            | stp.kwd('tail len')
            | stp.kwd('taillength')
            | stp.kwd('taillen')
            | stp.kwd('tail')
            | stp.kwd('tal')
            | char_key
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
        if parts.get('shorthand_tal') is not None:
            return self.shorthand_length(match, parts, 'shorthand_tal')
        if parts.get('numerator') is not None:
            return self.fraction(match, parts)
        return self.simple(match, parts)

    def fix_up_result(self, text, result):
        """Fix problematic results."""
        start = max(0, result.start - LOOKBACK)
        if IS_TESTES.search(text, start, result.start):
            return None
        if IS_CROSS.search(text, result.end):
            return None
        return self.fix_up_inches(text, result)
