"""Parse body mass notations."""

from pyparsing import Regex, Word
from pyparsing import CaselessLiteral as lit
from lib.base_trait import BaseTrait
from lib.numeric_trait_mix_in import NumericTraitMixIn
from lib.parse_result import ParseResult
import lib.shared_parser_patterns as sp


class BodyMass(BaseTrait, NumericTraitMixIn):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        key_with_units = sp.kwd('weightingrams') | sp.kwd('massingrams')

        key_leader = lit('body') | lit('full') | lit('observed') | lit('total')
        weight = (
            lit('weights') | lit('weight') | lit('weighs') | lit('weighed')
            | lit('weighing')
        )
        key = (
            key_leader + weight
            | key_leader + sp.lit('mass')
            | weight
            | sp.kwd('mass')
            | sp.kwd('body')
        )

        key_with_dots = Regex(r' \b w \.? t s? \.? ', sp.flags)

        wt_key = key | key_with_dots

        parser = (
            key_with_units('units') + sp.pair
            | wt_key + sp.mass_units('units') + sp.pair
            | wt_key + sp.pair + sp.mass_units('units')
            | sp.shorthand_key + sp.pair + sp.mass_units('units')
            | sp.shorthand_key + sp.mass_units('units') + sp.pair
            | (wt_key
               + sp.number('lbs') + sp.pounds
               + sp.pair('ozs') + sp.ounces)
            | (sp.number('lbs') + sp.pounds + sp.pair('ozs') + sp.ounces
               )('ambiguous_key')
            | wt_key + sp.pair
            | sp.shorthand_key + sp.shorthand
            | sp.shorthand
        )

        parser.ignore(Word(sp.punct))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()

        if parts.get('shorthand_tl') is not None:
            return self.shorthand(match, parts)
        if parts.get('lbs') is not None:
            return self.compound(match, parts, ['lbs', 'ozs'])
        return self.simple(match, parts)

    def shorthand(self, match, parts):
        """Convert a shorthand value like 11-22-33-44:55g."""
        result = ParseResult()
        result.float_value(parts.get('shorthand_wt'))
        if not result.value:
            return None
        result.convert_value(parts.get('shorthand_wt_units'))
        result.is_flag_in_dict(parts, 'shorthand_wt_amb', 'estimated_value')
        result.ends(match[1], match[2])
        return result
