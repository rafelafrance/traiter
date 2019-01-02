"""Parse testes state notations."""

from pyparsing import Regex, Word, Group, Optional
from lib.parsers.base import Base
import lib.parsers.regexp as rx


class TestesState(Base):
    """Parser logic."""

    def build_parser(self):  # pylint: disable=too-many-locals
        """Return the trait parser."""
        label = Regex(
            rx.boundary(r' reproductive .? (?: data | state | condition ) '),
            rx.flags)
        testes = Regex(
            rx.boundary(r' testes |  testis | testicles '),
            rx.flags)
        fully = Regex(
            rx.boundary(r' fully | (:? in ) complete (?: ly) '),
            rx.flags)
        non = Regex(
            rx.boundary(r' not | non | no | semi | sub '),
            rx.flags)
        descended = Regex(
            rx.boundary(r' (?: un)? (?: des?c?end (?: ed)? | desc ) '),
            rx.flags)
        abbrev = Regex(
            rx.boundary(r' tes | ts | t '),
            rx.flags)
        scrotal = Regex(
            rx.boundary(r' scrotum | scrotal | scrot '),
            rx.flags)
        partially = Regex(
            rx.boundary(r' partially | part '),
            rx.flags)
        state_abbrev = Regex(
            rx.boundary(r' scr | ns | sc'),
            rx.flags)
        abdominal = Regex(
            rx.boundary(r' abdominal | abdomin | abdom '),
            rx.flags)
        size = Regex(
            rx.boundary(r' visible | enlarged | small '),
            rx.flags)
        gonads = Regex(
            rx.boundary(r' gonads? '),
            rx.flags)
        other = Regex(
            rx.boundary(r""" cryptorchism | cryptorchid | monorchism
                                | monorchid | nscr | inguinal"""),
            rx.flags)
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

        ignore = Word(rx.punct)
        parser.ignore(ignore)
        return parser
