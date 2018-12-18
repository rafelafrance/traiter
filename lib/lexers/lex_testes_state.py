"""Lex testes state annotations."""

# pylint: disable=too-few-public-methods

from lib.lexers.lex_base import LexBase, LexRule, LexRules


class LexTestesState(LexBase):
    """Lex testes state annotations."""

    def rule_list(self) -> LexRules:
        return [
            self.stop,

            LexRule(
                'label',
                self.boundary(
                    r""" reproductive .? (?: data |state | condition ) """)),

            LexRule(
                'testes', self.boundary(r' testes |  testis | testicles ')),

            LexRule(
                'fully',
                self.boundary(r' fully | (:? in ) complete (?: ly) ')),

            LexRule('not', self.boundary(r' not | non | no | semi | sub ')),

            LexRule(
                'descended',
                self.boundary(r' (?: un)? (?: des?c?end (?: ed)? | desc ) ')),

            LexRule('abbrev', self.boundary(r' tes | ts | t ')),

            LexRule(
                'scrotal',
                self.boundary(r' scrotum | scrotal | scrot ')),

            LexRule('partially', self.boundary(r' partially | part ')),

            LexRule(
                'other_words',
                self.boundary(
                    r""" cryptorchism | cryptorchid | monorchism | monorchid
                        | nscr | inguinal""")),

            LexRule('state_abbrev', self.boundary(r' scr | ns | sc')),

            LexRule('abdominal',
                    self.boundary(r' abdominal | abdomin | abdom ')),

            LexRule('size', self.boundary(r' visible | enlarged | small ')),

            LexRule('gonads', self.boundary(r' gonads? ')),
        ]
