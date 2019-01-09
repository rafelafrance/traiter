"""Parse total length notations."""

from pyparsing import Regex, Word, alphas, alphanums
from pyparsing import CaselessLiteral as lit
from lib.base_trait import BaseTrait
from lib.numeric_trait_mix_in import NumericTraitMixIn
import lib.shared_trait_patterns as stp


class TotalLength(BaseTrait, NumericTraitMixIn):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        words = Word(alphas, alphanums)*(1, 3)

        key_with_units = (
            stp.kwd('totallengthinmillimeters')
            | stp.kwd('totallengthinmm')
            | stp.kwd('total length in millimeters')
            | stp.kwd('total length in mm')
            | stp.kwd('snoutventlengthinmillimeters')
            | stp.kwd('snoutventlengthinmm')
            | stp.kwd('snoutvent length in millimeters')
            | stp.kwd('snoutvent length in mm')
            | stp.kwd('headbodylengthinmillimeters')
            | stp.kwd('headbodylengthinmm')
            | stp.kwd('headbody length in millimeters')
            | stp.kwd('headbody length in mm')
            | stp.kwd('forklengthinmillimeters')
            | stp.kwd('forklengthinmm')
            | stp.kwd('fork length in millimeters')
            | stp.kwd('fork length in mm')
        )

        len_key = Regex(r"""
            total  [\s-]* length [\s-]* in
            | (?: total | max | standard ) [\s-]* lengths?
            | meas [\s*:]? \s* length [\s(]* [l] [)\s:]*
            | meas (?: [a-z]* )? \.? : \s* L
            | t [o.]? l \.? _?
            | s \.? l \.?
            | label [\s.]* lengths?
            | (?: fork | mean | body ) [\s-]* lengths?
            | s \.? v \.? ( l \.? )?
            | snout [\s-]* vent [\s-]* lengths?
            """, stp.flags)

        ambiguous = Regex(r'(?<! [a-z] )(?<! [a-z] \s ) lengths? ', stp.flags)

        key_units_req = (
            lit('measurements') | lit('measurement')
            | lit('body')
            | lit('total')
        )

        parser = (
            key_with_units('units') + stp.pair

            | stp.shorthand_key + stp.pair + stp.len_units('units')
            | stp.shorthand_key + stp.len_units('units') + stp.pair

            | key_units_req + stp.fraction + stp.len_units('units')
            | key_units_req + stp.pair + stp.len_units('units')

            | len_key + stp.fraction + stp.len_units('units')
            | (ambiguous + stp.fraction + stp.len_units('units')
               )('ambiguous_key')

            | stp.pair + stp.len_units('units') + len_key
            | stp.pair + len_key

            | (len_key
               + stp.pair('ft') + stp.feet('ft_units')
               + stp.pair('in') + stp.inches('in_units'))
            | (stp.pair('ft') + stp.feet('ft_units')
               + stp.pair('in') + stp.inches('in_units'))('ambiguous_key')

            # Due to trailing len_key the leading key it is no longer ambiguous
            | ambiguous + stp.pair + stp.len_units('units') + len_key
            | ambiguous + stp.pair + len_key

            | (ambiguous + stp.pair + stp.len_units('units'))('ambiguous_key')
            | (ambiguous + stp.len_units('units') + stp.pair)('ambiguous_key')
            | (ambiguous + stp.pair)('ambiguous_key')

            | stp.shorthand_key + stp.shorthand
            | stp.shorthand

            | len_key + stp.pair + stp.len_units('units')
            | len_key + stp.len_units('units') + stp.pair
            | len_key + stp.pair
            | len_key + words + stp.pair + stp.len_units('units')
            | len_key + words + stp.pair
        )

        parser.ignore(Word(stp.punct, excludeChars=';/'))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()
        if parts.get('shorthand_tl') is not None:
            return self.shorthand_length(match, parts, 'shorthand_tl')
        if parts.get('ft') is not None:
            return self.compound(match, parts, ['ft', 'in'])
        if parts.get('numerator') is not None:
            return self.fraction(match, parts)
        return self.simple(match, parts)
