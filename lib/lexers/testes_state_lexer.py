"""Lex testes state annotations."""

from lib.lexers.base_lexer import BaseLexer, build


class LexerTestesState(BaseLexer):
    """Lex testes state annotations."""

    tokens = [
        BaseLexer.stop,  # We don't want to confuse prefix and suffix notation

        ('label',
         build(r' reproductive .? (?: data |state | condition ) ')),

        ('testes',
         build(r' testes |  testis | testicles ')),

        ('fully',
         build(r' fully | (:? in ) complete (?: ly) ')),

        ('not',
         build(r' not | non | no | semi | sub ')),

        ('descended',
         build(r' (?: un)? (?: des?c?end (?: ed)? | desc ) ')),

        ('abbrev',
         build(r' tes | ts | t ')),

        ('scrotal',
         build(r' scrotum | scrotal | scrot ')),

        ('partially',
         build(r' partially | part ')),

        ('other_words',
         build((r' cryptorchism | cryptorchid | monorchism | monorchid '
                r' | nscr | inguinal'))),

        ('state_abbrev',
         build(r' scr | ns | sc')),

        ('abdominal',
         build(r' abdominal | abdomin | abdom ')),

        ('size',
         build(r' visible | enlarged | small ')),

        ('gonads',
         build(r' gonads? '))]
