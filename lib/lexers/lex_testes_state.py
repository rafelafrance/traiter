"""Lex testes state annotations."""

# pylint: disable=too-few-public-methods

from lib.lexers.lex_base import LexBase
import lib.lexers.shared_lex_rules as rule
import lib.lexers.shared_utils as util


class LexTestesState(LexBase):
    """Lex testes state annotations."""

    def rule_list(self) -> rule.LexRules:
        return [
            rule.stop,

            rule.LexRule(
                'label',
                util.boundary(
                    r""" reproductive .? (?: data |state | condition ) """)),

            rule.LexRule(
                'testes', util.boundary(r' testes |  testis | testicles ')),

            rule.LexRule(
                'fully',
                util.boundary(r' fully | (:? in ) complete (?: ly) ')),

            rule.LexRule(
                'not', util.boundary(r' not | non | no | semi | sub ')),

            rule.LexRule(
                'descended',
                util.boundary(r' (?: un)? (?: des?c?end (?: ed)? | desc ) ')),

            rule.LexRule('abbrev', util.boundary(r' tes | ts | t ')),

            rule.LexRule(
                'scrotal',
                util.boundary(r' scrotum | scrotal | scrot ')),

            rule.LexRule('partially', util.boundary(r' partially | part ')),

            rule.LexRule(
                'other_words',
                util.boundary(
                    r""" cryptorchism | cryptorchid | monorchism | monorchid
                        | nscr | inguinal""")),

            rule.LexRule('state_abbrev', util.boundary(r' scr | ns | sc')),

            rule.LexRule(
                'abdominal', util.boundary(r' abdominal | abdomin | abdom ')),

            rule.LexRule(
                'size', util.boundary(r' visible | enlarged | small ')),

            rule.LexRule('gonads', util.boundary(r' gonads? ')),
        ]
