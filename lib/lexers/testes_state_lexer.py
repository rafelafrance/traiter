"""Lex testes state annotations."""

# pylint: disable=too-few-public-methods

from lib.lexers.base_lexer import BaseLexer, isolate


class LexerTestesState(BaseLexer):
    """Lex testes state annotations."""

    tokens = [
        BaseLexer.stop,  # We don't want to confuse prefix and suffix notation

        ('label',
         isolate(r' reproductive .? (?: data |state | condition ) ')),

        ('testes',
         isolate(r' testes |  testis | testicles ')),

        ('fully',
         isolate(r' fully | (:? in ) complete (?: ly) ')),

        ('not',
         isolate(r' not | non | no | semi | sub ')),

        ('descended',
         isolate(r' (?: un)? (?: des?c?end (?: ed)? | desc ) ')),

        ('abbrev',
         isolate(r' tes | ts | t ')),

        ('scrotal',
         isolate(r' scrotum | scrotal | scrot ')),

        ('partially',
         isolate(r' partially | part ')),

        ('other_words',
         isolate((r' cryptorchism | cryptorchid | monorchism | monorchid '
                  r' | nscr | inguinal'))),

        ('state_abbrev',
         isolate(r' scr | ns | sc')),

        ('abdominal',
         isolate(r' abdominal | abdomin | abdom ')),

        ('size',
         isolate(r' visible | enlarged | small ')),

        ('gonads',
         isolate(r' gonads? '))]
