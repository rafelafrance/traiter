"""Parse testes size notations."""

from pyparsing import Regex, Word, alphas
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

        ambiguous_sex = Regex(
            rx.boundary(r"""
                gonad \s? length \s? (?P<index> [12] )
                | (?P<units> gonad \s?
                    (?: length | width ) \s? in \s? mm )
                | (?P<side> left | right ) \s? gonad \s? (?: length | width )
                """), rx.flags)('ambiguous_sex')

        testes = (rx.kwd('testicles') | rx.kwd('testes') | rx.kwd('testis')
                  | rx.kwd('test'))

        abbrev = rx.kwd('tes') | rx.kwd('ts') | rx.kwd('t')

        scrotal = rx.kwd('scrotum') | rx.kwd('scrotal') | rx.kwd('scrot')

        parser = (
            label + (testes | abbrev) + rx.cross
            | label + rx.cross
            | label + testes + rx.cross
            | label + words + rx.cross
            | label + words + rx.cross
            | ambiguous_sex + rx.cross
            | ambiguous_sex + rx.cross
            | ambiguous_sex + words + rx.cross
            | ambiguous_sex + words + rx.cross
            | testes + rx.cross
            | testes + words + rx.cross
            | scrotal + rx.cross
        )

        ignore = Word(rx.punct)
        parser.ignore(ignore)
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()
        result = Result()
        result.cross_value(parts)
        result.flag_from_dict(parts, 'index')
        result.flag_from_dict(parts, 'side')
        result.is_flag_in_dict(parts, 'ambiguous_sex')
        result.ends(match[1], match[2])
        return result
