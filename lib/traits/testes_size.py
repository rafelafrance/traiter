"""Parse testes size notations."""

from pyparsing import Regex, Word, alphas
from lib.base import Base
from lib.result import Result
from lib.units import convert
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
                | (?P<millimeters> gonad \s?
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

        value = self.to_float(parts.get('value1'))
        value2 = self.to_float(parts.get('value2'))

        units = parts.get('units1')
        units2 = parts.get('units2')
        if parts.get('millimeters'):
            units = 'mm'

        value = convert(value, units)
        if value2 and units2:
            value2 = convert(value2, units2)
        elif value2:
            value2 = convert(value2, units)

        if value2:
            value = [value, value2]

        if units2 and units2 != units:
            units = [units, units2]

        flags = {}
        self.set_units_inferred(flags, units)
        self.set_flag(parts, flags, 'index')
        self.set_flag(parts, flags, 'side')
        self.set_flag(parts, flags, 'ambiguous_sex', as_bool=True)

        return Result(value=value, flags=flags, units=units,
                      start=match[1], end=match[2])
