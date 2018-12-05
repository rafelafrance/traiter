"""Lex testes state annotations."""

from lib.lexers.base_lexer import BaseLexer


class LexerTestesState(BaseLexer):
    """Lex testes state annotations."""

    forms = [
        ('reproductive_data',
         r'reproductive .? (?: data |state | condition )'),

        ('testes',
         r' testes |  testis | testicles '),

        ('fully',
         r' fully | (:? in ) complete (?: ly) '),

        ('not',
         r' (?: not | non | no | semi | sub) '),

        ('descended',
         r' (?: un)? (?: des?c?end (?: ed)? | desc ) '),

        ('testes_abbrev',
         r' tes | ts | t '),

        ('scrotal',
         r' scrot | scrotum | scrotal '),

        ('partially',
         r' partially | part '),

        ('other_words',
         (r'cryptorchism | cryptorchid | monorchism | monorchid '
          r'| nscr | inguinal')),

        ('state_abbrev',
         r'scr | ns | sc'),

        ('key_req',
         r'visible | enlarged | small | abdominal | abdomin | abdom'),

        # ('', r''),
    ]
