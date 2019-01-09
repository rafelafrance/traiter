"""Parse testes size notations."""

from pyparsing import Word, alphas, Group
from pyparsing import CaselessLiteral as lit
from lib.base import Base
from lib.result import Result
import lib.regexp as rx


class TestesSize(Base):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        words = Word(alphas)*(1, 3)

        label = (
            rx.kwd('reproductive')
            + (rx.kwd('data') | rx.kwd('state') | rx.kwd('condition'))
        )

        key_with_units = (
            Group(rx.kwd('gonad') + rx.kwd('length') + rx.kwd('in')
                  + rx.kwd('mm'))
            | Group(rx.kwd('gonad') + rx.kwd('length') + rx.kwd('in')
                    + rx.kwd('millimeters'))
            | Group(rx.kwd('gonad') + rx.kwd('width') + rx.kwd('in')
                    + rx.kwd('mm'))
            | Group(rx.kwd('gonad') + rx.kwd('width') + rx.kwd('in')
                    + rx.kwd('millimeters'))
            | rx.kwd('gonadlengthinmm')
            | rx.kwd('gonadlengthinmillimeters')
            | rx.kwd('gonadwidthinmm')
            | rx.kwd('gonadwidthinmillimeters')
        )('units')

        ambiguous = (
            rx.kwd('gonad') + rx.kwd('length') + Word('12', max=1)('index')
            | rx.kwd('gonad') + rx.kwd('width') + Word('12', max=1)('index')
            | lit('gonadlength') + Word('12', max=1)('index')
            | lit('gonadwidth') + Word('12', max=1)('index')
            | rx.kwd('left')('side') + rx.kwd('gonad') + rx.kwd('length')
            | rx.kwd('left')('side') + rx.kwd('gonad') + rx.kwd('width')
            | rx.kwd('right')('side') + rx.kwd('gonad') + rx.kwd('length')
            | rx.kwd('right')('side') + rx.kwd('gonad') + rx.kwd('width')
            | lit('left')('side') + lit('gonadlength')
            | lit('left')('side') + lit('gonadwidth')
            | lit('right')('side') + lit('gonadlength')
            | lit('right')('side') + lit('gonadwidth')
            | rx.kwd('gonad') + rx.kwd('length')
            | rx.kwd('gonad') + rx.kwd('width')
            | rx.kwd('gonadlength')
            | rx.kwd('gonadwidth')
        )

        ambiguous_sex = (key_with_units | ambiguous)('ambiguous_sex')

        testes = (rx.kwd('testicles') | rx.kwd('testes') | rx.kwd('testis')
                  | rx.kwd('test'))

        abbrev = rx.kwd('tes') | rx.kwd('ts') | rx.kwd('t')

        scrotal = rx.kwd('scrotum') | rx.kwd('scrotal') | rx.kwd('scrot')

        parser = (
            label + (testes | abbrev) + rx.cross
            | label + rx.cross
            | label + testes + rx.cross
            | label + words + rx.cross
            | ambiguous_sex + rx.cross
            | ambiguous_sex + words + rx.cross
            | testes + rx.cross
            | testes + words + rx.cross
            | scrotal + rx.cross
        )

        parser.ignore(Word(rx.punct))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()
        print(parts)
        result = Result()
        result.cross_value(parts)
        result.flag_from_dict(parts, 'index')
        result.flag_from_dict(parts, 'side')
        result.is_flag_in_dict(parts, 'ambiguous_sex')
        result.ends(match[1], match[2])
        return result
