"""Parse body mass notations."""

from pyparsing import Regex, Word
from pyparsing import CaselessLiteral as lit
from lib.base_trait import BaseTrait
from lib.numeric_trait_mixin import NumericTraitMixIn
from lib.parsed_trait import ParsedTrait
import lib.shared_trait_patterns as stp


class BodyMass(NumericTraitMixIn, BaseTrait):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        key_with_units = stp.kwd('weightingrams') | stp.kwd('massingrams')

        key_leader = lit('body') | lit('full') | lit('observed') | lit('total')
        weight = (
            lit('weights') | lit('weight') | lit('weighs') | lit('weighed')
            | lit('weighing')
        )
        key = (
            key_leader + weight
            | key_leader + stp.lit('mass')
            | weight
            | stp.kwd('mass')
            | stp.kwd('body')
        )

        key_with_dots = Regex(r' \b w \.? t s? \.? ', stp.flags)

        wt_key = key | key_with_dots

        parser = (
            key_with_units('units') + stp.pair
            | wt_key + stp.mass_units('units') + stp.pair
            | wt_key + stp.pair + stp.mass_units('units')
            | stp.shorthand_key + stp.pair + stp.mass_units('units')
            | stp.shorthand_key + stp.mass_units('units') + stp.pair
            | (wt_key
               + stp.number('lbs') + stp.pounds
               + stp.pair('ozs') + stp.ounces)
            | (stp.number('lbs') + stp.pounds + stp.pair('ozs') + stp.ounces
               )('ambiguous_key')
            | wt_key + stp.pair
            | stp.shorthand_key + stp.shorthand
            | stp.shorthand
        )

        parser.ignore(Word(stp.punct))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()

        if parts.get('shorthand_tl') is not None:
            return self.shorthand(match, parts)
        if parts.get('lbs') is not None:
            return self.compound(match, parts, ['lbs', 'ozs'])
        return self.simple(match, parts)

    @staticmethod
    def shorthand(match, parts):
        """Convert a shorthand value like 11-22-33-44:55g."""
        result = ParsedTrait()
        result.float_value(parts.get('shorthand_wt'))
        if not result.value:
            return None
        result.convert_value(parts.get('shorthand_wt_units'))
        result.is_flag_in_dict(parts, 'shorthand_wt_amb', 'estimated_value')
        result.ends(match[1], match[2])
        return result
