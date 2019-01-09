"""Parse testes state notations."""

from pyparsing import Regex, Word, Group, Optional
from lib.base import Base
from lib.result import Result
import lib.regexp as rx


class TestesState(Base):
    """Parser logic."""

    def build_parser(self):  # pylint: disable=too-many-locals
        """Return the trait parser."""
        label = (
            rx.kwd('reproductive')
            + (rx.kwd('data') | rx.kwd('state') | rx.kwd('condition'))
        )
        testes = (
            rx.kwd('testicles') | rx.kwd('testes') | rx.kwd('testis')
            | rx.kwd('test')
        )
        fully = (
            rx.kwd('fully') | rx.kwd('incompletely') | rx.kwd('completely')
            | rx.kwd('complete')
        )
        non = (
            rx.kwd('not') | rx.kwd('non') | rx.kwd('no') | rx.kwd('semi')
            | rx.kwd('sub')
        )
        descended = (
            rx.kwd('undescended') | rx.kwd('undescend') | rx.kwd('undesc')
            | rx.kwd('undes') | rx.kwd('descended') | rx.kwd('descend')
            | rx.kwd('desc') | rx.kwd('des') | rx.kwd('undecended')
            | rx.kwd('undecend') | rx.kwd('decended') | rx.kwd('decend')
            | rx.kwd('undesended') | rx.kwd('undesend') | rx.kwd('desended')
            | rx.kwd('desend')
        )
        abbrev = rx.kwd('tes') | rx.kwd('ts') | Regex(r'\b t \b', rx.flags)
        scrotal = rx.kwd('scrotum') | rx.kwd('scrotal') | rx.kwd('scrot')
        partially = rx.kwd('partially') | rx.kwd('part')
        state_abbrev = rx.kwd('scr') | rx.kwd('ns') | rx.kwd('sc')
        abdominal = rx.kwd('abdominal') | rx.kwd('abdomin') | rx.kwd('abdom')
        size = rx.kwd('visible') | rx.kwd('enlarged') | rx.kwd('small')
        gonads = (rx.kwd('gonads') | rx.kwd('gonad'))('ambiguous_sex')
        other = (
            rx.kwd('cryptorchism') | rx.kwd('cryptorchid')
            | rx.kwd('monorchism') | rx.kwd('monorchid')
            | rx.kwd('inguinal') | rx.kwd('nscr')
        )
        length = Optional(rx.cross + Optional(rx.len_units))

        state = (
            Group(non + fully + descended)
            | Group(abdominal + non + descended)
            | Group(abdominal + descended)
            | Group(non + descended)
            | Group(fully + descended)
            | Group(partially + descended)
            | Group(size + non + descended)
            | Group(size + descended)
            | descended
            | size
        )

        parser = (
            (label + (testes | abbrev) + length + state('value'))
            | (label + (testes | abbrev) + length + state_abbrev('value'))
            | (label + (testes | abbrev) + length + abdominal('value'))
            | (label + (testes | abbrev) + length + scrotal('value'))
            | (label + (testes | abbrev) + length + (non + scrotal)('value'))
            | (label + (testes | abbrev) + length + other('value'))
            | (label + (testes | abbrev) + length + (non + testes)('value'))
            | (label + length + (non + testes)('value'))
            | (label + length + (non + scrotal)('value'))
            | (label + length + scrotal('value'))
            | abbrev + length + state('value')
            | abbrev + length + abdominal('value')
            | abbrev + length + (non + scrotal)('value')
            | abbrev + length + scrotal('value')
            | abbrev + length + other('value')
            | testes + length + state('value')
            | testes + length + state_abbrev('value')
            | testes + length + abdominal('value')
            | testes + length + scrotal('value')
            | testes + length + (non + scrotal)('value')
            | testes + length + other('value')
            | (non + testes)('value')
            | (non + scrotal)('value')
            | (non + gonads)('value')
            | scrotal('value')
        )

        parser.ignore(Word(rx.punct))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()
        result = Result()
        result.vocabulary_value(parts['value'])
        result.is_flag_in_dict(parts, 'ambiguous_sex')
        result.ends(match[1], match[2])
        return result
