"""Lex testes state annotations."""

# pylint: disable=too-few-public-methods

from lib.lexers.base import Base
from lib.lexers.util import boundary


class LexTestesState(Base):
    """Lex testes state annotations."""

    tokens = [
        Base.stop,  # We don't want to confuse prefix and suffix notation

        ('label',
         boundary(
             r' reproductive .? (?: data |state | condition ) ')),

        ('testes',
         boundary(r' testes |  testis | testicles ')),

        ('fully',
         boundary(r' fully | (:? in ) complete (?: ly) ')),

        ('not',
         boundary(r' not | non | no | semi | sub ')),

        ('descended',
         boundary(r' (?: un)? (?: des?c?end (?: ed)? | desc ) ')),

        ('abbrev',
         boundary(r' tes | ts | t ')),

        ('scrotal',
         boundary(r' scrotum | scrotal | scrot ')),

        ('partially',
         boundary(r' partially | part ')),

        ('other_words',
         boundary(
             (r' cryptorchism | cryptorchid | monorchism | monorchid '
              r' | nscr | inguinal'))),

        ('state_abbrev',
         boundary(r' scr | ns | sc')),

        ('abdominal',
         boundary(r' abdominal | abdomin | abdom ')),

        ('size',
         boundary(r' visible | enlarged | small ')),

        ('gonads',
         boundary(r' gonads? '))]
