"""Lex sex annotations."""

# pylint: disable=too-few-public-methods

from lib.lexers.lex_base import LexBase, LexRule, LexRules


class LexSex(LexBase):
    """Lex testes state annotations."""

    def rule_list(self) -> LexRules:
        return [
            self.stop,

            LexRule('key', self.boundary(r' sex ')),

            LexRule('sex', self.boundary(r' males? | females? ')),

            LexRule('quest', r' \? '),

            # These are words that indicate "sex" is not a key
            LexRule('skip', self.boundary(r' and | is | was ')),

            self.word,
        ]
