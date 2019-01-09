"""Parse testes size notations."""

from pyparsing import Word, alphas, Group
from pyparsing import CaselessLiteral as lit
from lib.base_trait import BaseTrait
from lib.numeric_trait_mixin import NumericTraitMixIn
from lib.parse_result import ParseResult
import lib.shared_trait_patterns as stp


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
            Group(stp.kwd('gonad') + stp.kwd('length') + stp.kwd('in')
                  + stp.kwd('mm'))
            | Group(stp.kwd('gonad') + stp.kwd('length') + stp.kwd('in')
                    + stp.kwd('millimeters'))
            | Group(stp.kwd('gonad') + stp.kwd('width') + stp.kwd('in')
                    + stp.kwd('mm'))
            | Group(stp.kwd('gonad') + stp.kwd('width') + stp.kwd('in')
                    + stp.kwd('millimeters'))
            | stp.kwd('gonadlengthinmm')
            | stp.kwd('gonadlengthinmillimeters')
            | stp.kwd('gonadwidthinmm')
            | stp.kwd('gonadwidthinmillimeters')
        )('units')

        ambiguous = (
            stp.kwd('gonad') + stp.kwd('length') + Word('12', max=1)('index')
            | stp.kwd('gonad') + stp.kwd('width') + Word('12', max=1)('index')
            | lit('gonadlength') + Word('12', max=1)('index')
            | lit('gonadwidth') + Word('12', max=1)('index')
            | stp.kwd('left')('side') + stp.kwd('gonad') + stp.kwd('length')
            | stp.kwd('left')('side') + stp.kwd('gonad') + stp.kwd('width')
            | stp.kwd('right')('side') + stp.kwd('gonad') + stp.kwd('length')
            | stp.kwd('right')('side') + stp.kwd('gonad') + stp.kwd('width')
            | lit('left')('side') + lit('gonadlength')
            | lit('left')('side') + lit('gonadwidth')
            | lit('right')('side') + lit('gonadlength')
            | lit('right')('side') + lit('gonadwidth')
            | stp.kwd('gonad') + stp.kwd('length')
            | stp.kwd('gonad') + stp.kwd('width')
            | stp.kwd('gonadlength')
            | stp.kwd('gonadwidth')
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
        print(parts)
        result = ParseResult()
        result.cross_value(parts)
        result.flag_from_dict(parts, 'index')
        result.flag_from_dict(parts, 'side')
        result.is_flag_in_dict(parts, 'ambiguous_sex')
        result.ends(match[1], match[2])
        return result
