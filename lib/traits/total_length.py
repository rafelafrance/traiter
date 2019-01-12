"""Parse total length notations."""

from pyparsing import Regex, Word, alphas, alphanums, ParserElement
from pyparsing import CaselessLiteral as lit
from lib.base_trait import BaseTrait
from lib.numeric_trait_mixin import NumericTraitMixIn
import lib.shared_trait_patterns as stp

ParserElement.enablePackrat()


class TotalLength(NumericTraitMixIn, BaseTrait):
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

        key = Regex(r"""
            total  [\s-]* length [\s-]* in
            | (?: total | max | standard ) [\s-]* lengths? \b
            | meas [\s*:]? \s* length [\s(]* [l] [)\s:]*
            | meas (?: [a-z]* )? \.? : \s* l
            | t [o.]? l \.? _?
            | s \.? l \.?
            | label [\s.]* lengths? \b
            | (?: fork | mean | body ) [\s-]* lengths? \b
            | s \.? v \.? ( l \.? )?
            | snout [\s-]* vent [\s-]* lengths? \b
            | (?<! \w \s ) \b l (?! [a-z] )
            """, stp.flags)

        ambiguous = Regex(r'(?<! [a-z] )(?<! [a-z] \s ) lengths? ', stp.flags)

        key_units_req = (
            lit('measurements') | lit('measurement')
            | lit('body')
            | lit('total')
        )

        parser = (
            key_with_units('units') + stp.pair

            | stp.shorthand_key + stp.shorthand
            | stp.shorthand

            | stp.shorthand_key + stp.pair + stp.len_units('units')
            | stp.shorthand_key + stp.len_units('units') + stp.pair

            | key_units_req + stp.fraction + stp.len_units('units')
            | key_units_req + stp.pair + stp.len_units('units')

            | key + stp.fraction + stp.len_units('units')
            | (ambiguous + stp.fraction + stp.len_units('units')
               )('ambiguous_key')

            | stp.pair + stp.len_units('units') + key
            | stp.pair + key

            | (key
               + stp.pair('ft') + stp.feet('ft_units')
               + stp.pair('in') + stp.inches('in_units'))
            | (stp.pair('ft') + stp.feet('ft_units')
               + stp.pair('in') + stp.inches('in_units'))('ambiguous_key')

            # Due to trailing key the leading key it is no longer ambiguous
            | ambiguous + stp.pair + stp.len_units('units') + key
            | ambiguous + stp.pair + key

            | (ambiguous + stp.pair + stp.len_units('units'))('ambiguous_key')
            | (ambiguous + stp.len_units('units') + stp.pair)('ambiguous_key')
            | (ambiguous + stp.pair)('ambiguous_key')

            | key + stp.pair + stp.len_units('units')
            | key + stp.len_units('units') + stp.pair
            | key + stp.pair
            | key + words + stp.pair + stp.len_units('units')
            | key + words + stp.pair
        )

        parser.ignore(Word(stp.punct, excludeChars='/;'))
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

    def fix_up_result(self, text, result):
        """Fix problematic parses."""
        return self.fix_up_inches(text, result)
