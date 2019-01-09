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
        global JUNK
        key_with_units = (
            stp.kwd('taillengthinmillimeters')
            | stp.kwd('taillengthinmm')
            | stp.kwd('tail length in millimeters')
            | stp.kwd('tail length in mm')
        )

        char_key = Regex(r""" \b t """, stp.flags)('check_false_positive')

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

    @staticmethod
    def check_false_positive(text, result):
        """Check if the 'T' abbreviation is actually for testes."""
        start = max(0, result.start - LOOKBACK)
        if IS_TESTES.search(text, start, result.start):
            return None
        if IS_CROSS.search(text, result.end):
            return None
        return result
