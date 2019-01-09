"""Parse total length notations."""

from pyparsing import Regex, Word, alphas, alphanums
from pyparsing import CaselessLiteral as lit
from lib.base_trait import BaseTrait
from lib.numeric_trait_mix_in import NumericTraitMixIn
import lib.shared_parser_patterns as sp


class TotalLength(BaseTrait, NumericTraitMixIn):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        words = Word(alphas, alphanums)*(1, 3)

        key_with_units = (
            sp.kwd('totallengthinmillimeters')
            | sp.kwd('totallengthinmm')
            | sp.kwd('total length in millimeters')
            | sp.kwd('total length in mm')
            | sp.kwd('snoutventlengthinmillimeters')
            | sp.kwd('snoutventlengthinmm')
            | sp.kwd('snoutvent length in millimeters')
            | sp.kwd('snoutvent length in mm')
            | sp.kwd('headbodylengthinmillimeters')
            | sp.kwd('headbodylengthinmm')
            | sp.kwd('headbody length in millimeters')
            | sp.kwd('headbody length in mm')
            | sp.kwd('forklengthinmillimeters')
            | sp.kwd('forklengthinmm')
            | sp.kwd('fork length in millimeters')
            | sp.kwd('fork length in mm')
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
            """, sp.flags)

        ambiguous = Regex(r'(?<! [a-z] )(?<! [a-z] \s ) lengths? ', sp.flags)

        key_units_req = (
            lit('measurements') | lit('measurement')
            | lit('body')
            | lit('total')
        )

        parser = (
            key_with_units('units') + sp.pair

            | sp.shorthand_key + sp.pair + sp.len_units('units')
            | sp.shorthand_key + sp.len_units('units') + sp.pair

            | key_units_req + sp.fraction + sp.len_units('units')
            | key_units_req + sp.pair + sp.len_units('units')

            | len_key + sp.fraction + sp.len_units('units')
            | (ambiguous + sp.fraction + sp.len_units('units')
               )('ambiguous_key')

            | sp.pair + sp.len_units('units') + len_key
            | sp.pair + len_key

            | (len_key
               + sp.pair('ft') + sp.feet('ft_units')
               + sp.pair('in') + sp.inches('in_units'))
            | (sp.pair('ft') + sp.feet('ft_units')
               + sp.pair('in') + sp.inches('in_units'))('ambiguous_key')

            # Due to trailing len_key the leading key it is no longer ambiguous
            | ambiguous + sp.pair + sp.len_units('units') + len_key
            | ambiguous + sp.pair + len_key

            | (ambiguous + sp.pair + sp.len_units('units'))('ambiguous_key')
            | (ambiguous + sp.len_units('units') + sp.pair)('ambiguous_key')
            | (ambiguous + sp.pair)('ambiguous_key')

            | sp.shorthand_key + sp.shorthand
            | sp.shorthand

            | len_key + sp.pair + sp.len_units('units')
            | len_key + sp.len_units('units') + sp.pair
            | len_key + sp.pair
            | len_key + words + sp.pair + sp.len_units('units')
            | len_key + words + sp.pair
        )

        parser.ignore(Word(sp.punct, excludeChars=';/'))
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
