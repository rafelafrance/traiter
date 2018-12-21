"""Lex testes state annotations."""

# pylint: disable=too-few-public-methods

from lib.lexers.lex_base import LexBase
import lib.lexers.shared_regexp as regexp


class LexTestesState(LexBase):
    """Lex testes state annotations."""

    def rule_list(self) -> regexp.Regexps:
        return [
            regexp.sep,

            regexp.Regexp(
                'label',
                regexp.boundary(
                    r""" reproductive .? (?: data |state | condition ) """)),

            regexp.Regexp(
                'testes', regexp.boundary(r' testes |  testis | testicles ')),

            regexp.Regexp(
                'fully',
                regexp.boundary(r' fully | (:? in ) complete (?: ly) ')),

            regexp.Regexp(
                'not', regexp.boundary(r' not | non | no | semi | sub ')),

            regexp.Regexp(
                'descended',
                regexp.boundary(
                    r' (?: un)? (?: des?c?end (?: ed)? | desc ) ')),

            regexp.Regexp('abbrev', regexp.boundary(r' tes | ts | t ')),

            regexp.Regexp(
                'scrotal',
                regexp.boundary(r' scrotum | scrotal | scrot ')),

            regexp.Regexp('partially', regexp.boundary(r' partially | part ')),

            regexp.Regexp(
                'other_words',
                regexp.boundary(
                    r""" cryptorchism | cryptorchid | monorchism | monorchid
                        | nscr | inguinal""")),

            regexp.Regexp('state_abbrev', regexp.boundary(r' scr | ns | sc')),

            regexp.Regexp(
                'abdominal',
                regexp.boundary(r' abdominal | abdomin | abdom ')),

            regexp.Regexp(
                'size', regexp.boundary(r' visible | enlarged | small ')),

            regexp.Regexp('gonads', regexp.boundary(r' gonads? ')),
        ]
