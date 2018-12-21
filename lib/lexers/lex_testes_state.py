"""Lex testes state annotations."""

from lib.lexers.lex_base import LexBase
from lib.lexers.shared_regexp import Regexp, Regexps, get, boundary


class LexTestesState(LexBase):
    """Lex testes state annotations."""

    def rule_list(self) -> Regexps:
        """Define the lexer."""
        return [
            get('sep'),

            Regexp(
                'label',
                boundary(
                    r""" reproductive .? (?: data |state | condition ) """)),

            Regexp('testes', boundary(r' testes |  testis | testicles ')),

            Regexp('fully', boundary(r' fully | (:? in ) complete (?: ly) ')),

            Regexp('not', boundary(r' not | non | no | semi | sub ')),

            Regexp(
                'descended',
                boundary(r' (?: un)? (?: des?c?end (?: ed)? | desc ) ')),

            Regexp('abbrev', boundary(r' tes | ts | t ')),

            Regexp(
                'scrotal', boundary(r' scrotum | scrotal | scrot ')),

            Regexp('partially', boundary(r' partially | part ')),

            Regexp(
                'other_words',
                boundary(
                    r""" cryptorchism | cryptorchid | monorchism | monorchid
                        | nscr | inguinal""")),

            Regexp('state_abbrev', boundary(r' scr | ns | sc')),

            Regexp('abdominal', boundary(r' abdominal | abdomin | abdom ')),

            Regexp('size', boundary(r' visible | enlarged | small ')),

            Regexp('gonads', boundary(r' gonads? ')),
        ]
