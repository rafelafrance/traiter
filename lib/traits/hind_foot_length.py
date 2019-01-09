"""Parse hind foot length notations."""

# from pyparsing import Word
from lib.base_trait import BaseTrait
from lib.numeric_trait_mixin import NumericTraitMixIn
# import lib.shared_trait_patterns as stp


class HindFootLength(NumericTraitMixIn, BaseTrait):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        # parser.ignore(Word(stp.punct))
        # return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()
        if parts.get('shorthand_hfl') is not None:
            return self.shorthand_length(match, parts, 'shorthand_hfl')
        return self.simple(match, parts)
