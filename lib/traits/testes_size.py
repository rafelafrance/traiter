"""Parse testes size notations."""

from pyparsing import Word, alphas, Group
from pyparsing import CaselessLiteral as lit
from lib.base_trait import BaseTrait
from lib.parse_result import ParseResult
import lib.shared_parser_patterns as sp


class TestesSize(BaseTrait):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        words = Word(alphas)*(1, 3)

        label = (
            sp.kwd('reproductive')
            + (sp.kwd('data') | sp.kwd('state') | sp.kwd('condition'))
        )

        key_with_units = (
            Group(sp.kwd('gonad') + sp.kwd('length') + sp.kwd('in')
                  + sp.kwd('mm'))
            | Group(sp.kwd('gonad') + sp.kwd('length') + sp.kwd('in')
                    + sp.kwd('millimeters'))
            | Group(sp.kwd('gonad') + sp.kwd('width') + sp.kwd('in')
                    + sp.kwd('mm'))
            | Group(sp.kwd('gonad') + sp.kwd('width') + sp.kwd('in')
                    + sp.kwd('millimeters'))
            | sp.kwd('gonadlengthinmm')
            | sp.kwd('gonadlengthinmillimeters')
            | sp.kwd('gonadwidthinmm')
            | sp.kwd('gonadwidthinmillimeters')
        )('units')

        ambiguous = (
            sp.kwd('gonad') + sp.kwd('length') + Word('12', max=1)('index')
            | sp.kwd('gonad') + sp.kwd('width') + Word('12', max=1)('index')
            | lit('gonadlength') + Word('12', max=1)('index')
            | lit('gonadwidth') + Word('12', max=1)('index')
            | sp.kwd('left')('side') + sp.kwd('gonad') + sp.kwd('length')
            | sp.kwd('left')('side') + sp.kwd('gonad') + sp.kwd('width')
            | sp.kwd('right')('side') + sp.kwd('gonad') + sp.kwd('length')
            | sp.kwd('right')('side') + sp.kwd('gonad') + sp.kwd('width')
            | lit('left')('side') + lit('gonadlength')
            | lit('left')('side') + lit('gonadwidth')
            | lit('right')('side') + lit('gonadlength')
            | lit('right')('side') + lit('gonadwidth')
            | sp.kwd('gonad') + sp.kwd('length')
            | sp.kwd('gonad') + sp.kwd('width')
            | sp.kwd('gonadlength')
            | sp.kwd('gonadwidth')
        )

        ambiguous_sex = (key_with_units | ambiguous)('ambiguous_sex')

        testes = (sp.kwd('testicles') | sp.kwd('testes') | sp.kwd('testis')
                  | sp.kwd('test'))

        abbrev = sp.kwd('tes') | sp.kwd('ts') | sp.kwd('t')

        scrotal = sp.kwd('scrotum') | sp.kwd('scrotal') | sp.kwd('scrot')

        parser = (
            label + (testes | abbrev) + sp.cross
            | label + sp.cross
            | label + testes + sp.cross
            | label + words + sp.cross
            | ambiguous_sex + sp.cross
            | ambiguous_sex + words + sp.cross
            | testes + sp.cross
            | testes + words + sp.cross
            | scrotal + sp.cross
        )

        parser.ignore(Word(sp.punct))
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
