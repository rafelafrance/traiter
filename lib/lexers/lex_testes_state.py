"""Lex testes state annotations."""

# pylint: disable=too-few-public-methods

from lib.lexers.lex_base import LexBase, LexRule
from lib.lexers.util import boundary


class LexTestesState(LexBase):
    """Lex testes state annotations."""

    tokens = [
        LexBase.stop,  # We don't want to confuse prefix and suffix notation

        LexRule(
            'label',
            boundary(r' reproductive .? (?: data |state | condition ) ')),

        LexRule('testes', boundary(r' testes |  testis | testicles ')),

        LexRule('fully', boundary(r' fully | (:? in ) complete (?: ly) ')),

        LexRule('not', boundary(r' not | non | no | semi | sub ')),

        LexRule(
            'descended',
            boundary(r' (?: un)? (?: des?c?end (?: ed)? | desc ) ')),

        LexRule('abbrev', boundary(r' tes | ts | t ')),

        LexRule('scrotal', boundary(r' scrotum | scrotal | scrot ')),

        LexRule('partially', boundary(r' partially | part ')),

        LexRule(
            'other_words',
            boundary(
                (r' cryptorchism | cryptorchid | monorchism | monorchid '
                 r' | nscr | inguinal'))),

        LexRule('state_abbrev', boundary(r' scr | ns | sc')),

        LexRule('abdominal', boundary(r' abdominal | abdomin | abdom ')),

        LexRule('size', boundary(r' visible | enlarged | small ')),

        LexRule('gonads', boundary(r' gonads? '))]
