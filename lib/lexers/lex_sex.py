"""Lex sex annotations."""

# pylint: disable=too-few-public-methods

from lib.lexers.lex_base import LexBase
import lib.lexers.shared_lex_rules as rule
import lib.lexers.shared_utils as util


class LexSex(LexBase):
    """Lex testes state annotations."""

    def rule_list(self) -> rule.LexRules:
        return [
            rule.stop,

            rule.LexRule('key', util.boundary(r' sex ')),

            rule.LexRule('sex', util.boundary(r' males? | females? ')),

            rule.LexRule('quest', r' \? '),

            # These are words that indicate "sex" is not a key
            rule.LexRule('skip', util.boundary(r' and | is | was ')),

            rule.word,
        ]
