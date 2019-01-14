"""Parse testes size notations."""

from pyparsing import Word, alphas, ParserElement
from pyparsing import CaselessLiteral as lit
from lib.base_trait import BaseTrait
from lib.numeric_trait_mixin import NumericTraitMixIn
from lib.parsed_trait import ParsedTrait
import lib.shared_trait_patterns as stp

ParserElement.enablePackrat()


class TestesSize(NumericTraitMixIn, BaseTrait):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        words = Word(alphas)*(1, 3)

        label = (
            stp.kwd('reproductive')
            + (stp.kwd('data') | stp.kwd('state') | stp.kwd('condition'))
        )

        key_with_units = (
            (stp.kwd('gonad') + stp.kwd('length')('dimension')
             + stp.kwd('in') + stp.kwd('mm')('units'))
            | (stp.kwd('gonad') + stp.kwd('length')('dimension')
               + stp.kwd('in') + stp.kwd('millimeters')('units'))
            | (stp.kwd('gonad') + stp.kwd('width')('dimension')
               + stp.kwd('in') + stp.kwd('mm')('units'))
            | (stp.kwd('gonad') + stp.kwd('width')('dimension')
               + stp.kwd('in') + stp.kwd('millimeters')('units'))
            | (lit('gonad') + lit('length')('dimension')
               + lit('in') + lit('mm')('units'))
            | (lit('gonad') + lit('length')('dimension')
               + lit('in') + lit('millimeters')('units'))
            | (lit('gonad') + lit('width')('dimension')
               + lit('in') + lit('mm')('units'))
            | (lit('gonad') + lit('width')('dimension')
               + lit('in') + lit('millimeters')('units'))
        )

        ambiguous = (
            (stp.kwd('gonad') + stp.kwd('length')('dimension')
             + Word('12', max=1)('index'))
            | (stp.kwd('gonad') + stp.kwd('width')('dimension')
               + Word('12', max=1)('index'))
            | (lit('gonad') + lit('length')('dimension')
               + Word('12', max=1)('index'))
            | (lit('gonad') + lit('width')('dimension')
               + Word('12', max=1)('index'))
            | (stp.kwd('left')('side') + stp.kwd('gonad')
               + stp.kwd('length')('dimension'))
            | (stp.kwd('left')('side') + stp.kwd('gonad')
               + stp.kwd('width')('dimension'))
            | (stp.kwd('right')('side') + stp.kwd('gonad')
               + stp.kwd('length')('dimension'))
            | (stp.kwd('right')('side') + stp.kwd('gonad')
               + stp.kwd('width')('dimension'))
            | lit('left')('side') + lit('gonad') + lit('length')('dimension')
            | lit('left')('side') + lit('gonad') + lit('width')('dimension')
            | lit('right')('side') + lit('gonad') + lit('length')('dimension')
            | lit('right')('side') + lit('gonad') + lit('width')('dimension')
            | stp.kwd('gonad') + stp.kwd('length')('dimension')
            | stp.kwd('gonad') + stp.kwd('width')('dimension')
            | stp.kwd('gonad') + lit('length')('dimension')
            | stp.kwd('gonad') + lit('width')('dimension')
        )

        ambiguous_sex = (key_with_units | ambiguous)('ambiguous_sex')

        testes = (stp.kwd('testicles') | stp.kwd('testes') | stp.kwd('testis')
                  | stp.kwd('test'))

        abbrev = stp.kwd('tes') | stp.kwd('ts') | stp.kwd('t')

        scrotal = stp.kwd('scrotum') | stp.kwd('scrotal') | stp.kwd('scrot')

        parser = (
            label + (testes | abbrev) + stp.cross
            | label + stp.cross
            | label + testes + stp.cross
            | label + words + stp.cross
            | ambiguous_sex + stp.cross
            | ambiguous_sex + words + stp.cross
            | testes + stp.cross
            | testes + words + stp.cross
            | scrotal + stp.cross
        )

        parser.ignore(Word(stp.punct))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()
        result = ParsedTrait()
        result.cross_value(parts)
        result.flag_from_dict(parts, 'index')
        result.flag_from_dict(parts, 'side')
        result.flag_from_dict(parts, 'dimension')
        result.is_flag_in_dict(parts, 'ambiguous_sex')
        result.ends(match[1], match[2])
        return result
